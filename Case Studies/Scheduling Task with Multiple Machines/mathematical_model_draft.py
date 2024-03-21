import os
import Gantt_Chart as gc
import pyomo.opt as pyopt
import pyomo.environ as pyo
import pandas as pd
import functions as funcs


def main(time_limit=90, counter_limit=30, tolerance=1, focus=0, termination_gap=0, hard_time_limit=90):
    bigM = 24 * 20
    ultimatum = 24 * 3
    deadline = 24 * 2

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 8000)

    major_set_up = pd.read_csv("major_setup_times.csv", header=0, index_col=0)
    relevant_data = pd.read_csv("relevant_data.csv", header=0, index_col=0)

    m = pyo.ConcreteModel(name="Mathematical Model")
    m.fp = pyo.Set(initialize=[1, 2, 3])
    m.fl = pyo.Set(initialize=[4])
    m.f = pyo.Set(initialize=list(m.fl) + list(m.fp))
    m.j = pyo.Set(m.f, initialize={f: relevant_data[relevant_data["Type"] == f].index.to_list() for f in m.f})
    m.jfl = funcs.get_j_set(m, m.fl)
    m.jfp = funcs.get_j_set(m, m.fp)
    m.jf = funcs.get_j_set(m, m.f)

    m.l = pyo.Set(initialize=[1, 2, 3])
    m.p = pyo.Set(initialize=[4, 5])
    m.mc = pyo.Set(initialize=list(m.l) + list(m.p))
    m.t = pyo.Set(m.mc, initialize={
        mc: list(range(1, 7 + 1)) if mc in m.l else list(range(1, 9 + 1)) for mc in m.mc})
    m.tml = funcs.get_t_set(m, m.l)
    m.tmp = funcs.get_t_set(m, m.p)
    m.tmc = funcs.get_t_set(m, m.mc)

    m.w = pyo.Param(m.jf,
                    initialize=funcs.get_job_data(m, relevant_data, "Weight"))
    m.P_minor = pyo.Param(m.jf,
                          initialize=funcs.get_job_data(m, relevant_data, "Minor Setup Time"))
    m.P_major = pyo.Param(m.f, m.f, initialize={(f, g): major_set_up.loc[f, str(g)] for f in m.f for g in m.f})
    m.RC = pyo.Param(m.mc, initialize={mc: v for mc, v in zip(m.mc, [1, 0.95, 0.9, 0.95, 0.9])})
    m.SC = pyo.Param(m.mc, initialize={mc: v for mc, v in zip(m.mc, [1, 1, 1, 0.5, 0.5])})
    m.Capacity = pyo.Param(m.jf, m.mc,
                           initialize=funcs.get_job_data(m, relevant_data, "Capacity of Line 1", True))
    m.Demand = pyo.Param(m.jf, initialize=funcs.get_job_data(m, relevant_data, "Demand"))

    labor_dict = funcs.get_job_data(m, relevant_data, "Number of Labor Required")
    m.Labor = pyo.Param(m.jf, m.mc,
                        initialize={(j, f, mc): labor_dict[(j, f)] if mc in m.l else (12 if mc == 4 else 15) for
                                    j, f in m.jf for mc in m.mc})

    m.x = pyo.Var(m.jf, m.tmc, initialize=0, domain=pyo.Binary, doc="X(j,f,t,m)")
    m.y = pyo.Var(m.f, m.tmc, initialize=0, domain=pyo.Binary, doc="Y(g, t, m)")
    m.c_jt = pyo.Var(m.jf, m.tmc, initialize=0, domain=pyo.NonNegativeReals, doc="C(j, f, t, m)")
    m.c_j = pyo.Var(m.jf, initialize=0, domain=pyo.NonNegativeReals, doc="C(j, f)")
    m.s_jt = pyo.Var(m.jf, m.tmc, initialize=0, domain=pyo.NonNegativeReals, doc="S(j, f, t, m)")

    m.c_max = pyo.Var(domain=pyo.NonNegativeReals, doc="Max Completion Time")
    m.flow_time = pyo.Var(domain=pyo.NonNegativeReals, doc="Flow Time")
    m.w_flow_time = pyo.Var(domain=pyo.NonNegativeReals, doc="Weighted Flow Time")
    m.tardiness_quantity = pyo.Var(m.jf, domain=pyo.NonNegativeReals)
    m.tardiness = pyo.Var(domain=pyo.NonNegativeReals, doc="Total Tardiness")
    m.w_tardiness = pyo.Var(domain=pyo.NonNegativeReals, doc="Weighted Tardiness")
    m.tardy_binary = pyo.Var(m.jf, domain=pyo.Binary, initialize=0)
    m.tardy_jobs = pyo.Var(domain=pyo.NonNegativeReals, doc="Number of Tardy Jobs")
    m.w_tardy_jobs = pyo.Var(domain=pyo.NonNegativeReals, doc="Weighted Number of Tardy Jobs")

    def job_position_constraint(mo, j, f):
        return sum([m.x[(j, f, t, mc)] for (t, mc) in m.tml]) == 1

    m.job_position_constraint = pyo.Constraint(m.jf, rule=job_position_constraint)

    def job_position_constraint_packaging(mo, j, f):
        return sum([m.x[(j, f, t, mc)] for (t, mc) in m.tmp]) == 1

    m.job_position_constraint_packaging = pyo.Constraint(m.jfp, rule=job_position_constraint_packaging)

    def job_position_constraint_production(mo, j, f):
        return sum([m.x[(j, f, t, mc)] for (t, mc) in m.tmp]) == 0

    m.job_position_constraint_production = pyo.Constraint(m.jfl, rule=job_position_constraint_production)

    def position_job_constraint(mo, t, mc):
        return sum([m.x[(j, f, t, mc)] for (j, f) in m.jf]) <= 1

    m.position_job_constraint = pyo.Constraint(m.tmc, rule=position_job_constraint)

    def position_sequence_constraint(mo, j, f, t, mc):
        if t > 1:
            return m.x[(j, f, t, mc)] <= sum([m.x[(i, g, t - 1, mc)] if i != j else 0 for (i, g) in m.jf])
        else:
            return pyo.Constraint.Feasible

    m.position_sequence_constraint = pyo.Constraint(m.jf, m.tmc, rule=position_sequence_constraint)

    def completion_time_constraint(mo, j, f):
        return m.c_j[(j, f)] >= sum([m.c_jt[(j, f, t, mc)] for (t, mc) in m.tmc])

    m.completion_time_constraint = pyo.Constraint(m.jf, rule=completion_time_constraint)

    def completion_time_jt_constraint(mo, j, f, t, mc):
        return m.c_jt[(j, f, t, mc)] >= (sum([m.s_jt[(i, g, t, mc)] for (i, g) in m.jf]) +
                                         m.Demand[(j, f)] / m.Capacity[(j, f, mc)] -
                                         bigM * (1 - m.x[j, f, t, mc])
                                         )

    m.completion_time_jt_constraint = pyo.Constraint(m.jf, m.tmc,
                                                     rule=completion_time_jt_constraint)

    def start_time_jt_constraint(mo, j, f, t, mc):
        if t > 1:
            return m.s_jt[(j, f, t, mc)] >= (sum([m.c_jt[(i, g, t - 1, mc)] for (i, g) in m.jf]) +
                                             m.P_minor[(j, f)] * m.SC[mc] +
                                             sum([m.P_major[(f, g)] * m.SC[mc] * m.y[(g, t, mc)] for g in m.f]) -
                                             bigM * (1 - m.x[j, f, t, mc])
                                             )
        else:
            return m.s_jt[(j, f, t, mc)] >= (m.P_minor[(j, f)] * m.SC[mc] +
                                             sum([m.P_major[(f, g)] * m.SC[mc] * m.y[(g, t, mc)] for g in m.f]) -
                                             bigM * (1 - m.x[j, f, t, mc])
                                             )

    m.start_time_jt_constraint = pyo.Constraint(m.jf, m.tmc,
                                                rule=start_time_jt_constraint)

    def start_time_package_constraint(mo, j, f, t, mc):
        return m.s_jt[(j, f, t, mc)] >= (sum([m.s_jt[(j, f, tau, l)] for (tau, l) in m.tml]) +
                                         m.P_minor[j, f] * m.SC[mc] +
                                         sum([m.P_major[(f, g)] * m.SC[mc] * m.y[(g, t, mc)] for g in m.fp]) -
                                         bigM * (1 - m.x[j, f, t, mc])
                                         )

    m.start_time_package_constraint = pyo.Constraint(m.jfp, m.tmp,
                                                     rule=start_time_package_constraint)

    # Deactivated since all C_max were under 72 hours
    # def completion_time_limit_constraint(mo, j, f):
    #     return m.c_max <= ultimatum
    #
    # m.completion_time_limit_constraint = pyo.Constraint(m.jf, rule=completion_time_limit_constraint)

    def major_setup_constraint(mo, f, g, t, mc):
        if t > 1 and f != g:
            return m.y[g, t, mc] >= sum([m.x[i, g, t - 1, mc] for i in m.j[g]])
        else:
            return pyo.Constraint.Feasible

    m.major_setup_constraint = pyo.Constraint(m.f, m.f, m.tmc, rule=major_setup_constraint)

    def c_max_constraint(mo, j, f):
        return m.c_max >= m.c_j[(j, f)]

    m.c_max_constraint = pyo.Constraint(m.jf, rule=c_max_constraint)

    def flow_time_constraint(mo):
        return m.flow_time >= sum([m.c_j[(j, f)] for j, f in m.jf])

    m.flow_time_constraint = pyo.Constraint(rule=flow_time_constraint)

    def w_flow_time_constraint(mo):
        return m.w_flow_time >= sum([m.w[(j, f)] * m.c_j[(j, f)] for j, f in m.jf])

    m.w_flow_time_constraint = pyo.Constraint(rule=w_flow_time_constraint)

    def tardiness_quantity_constraint(mo, j, f):
        return m.tardiness_quantity[(j, f)] >= m.c_j[(j, f)] - deadline

    m.tardiness_quantity_constraint = pyo.Constraint(m.jf, rule=tardiness_quantity_constraint)

    def tardiness_constraint(mo):
        return m.tardiness >= sum([m.tardiness_quantity[(j, f)] for j, f in m.jf])

    m.tardiness_constraint = pyo.Constraint(rule=tardiness_constraint)

    def w_tardiness_constraint(mo):
        return m.w_tardiness >= sum([m.w[(j, f)] * m.tardiness_quantity[(j, f)] for j, f in m.jf])

    m.w_tardiness_constraint = pyo.Constraint(rule=w_tardiness_constraint)

    def tardy_constraint(mo, j, f):
        return bigM * m.tardy_binary[(j, f)] >= m.tardiness_quantity[(j, f)]

    m.tardy_constraint = pyo.Constraint(m.jf, rule=tardy_constraint)

    def tardy_jobs_constraint(mo):
        return m.tardy_jobs >= sum([m.tardy_binary[(j, f)] for (j, f) in m.jf])

    m.tardy_jobs_constraint = pyo.Constraint(rule=tardy_jobs_constraint)

    def w_tardy_jobs_constraint(mo):
        return m.w_tardy_jobs >= sum([m.w[(j, f)] * m.tardy_binary[(j, f)] for (j, f) in m.jf])

    m.w_tardy_jobs_constraint = pyo.Constraint(rule=w_tardy_jobs_constraint)

    callback = funcs.CallbackFunction(time_limit=time_limit, counter_limit=counter_limit, tolerance=tolerance)
    opt = pyopt.SolverFactory('gurobi_persistent', solver_io="python")
    opt.options["MIPFocus"] = focus
    opt.options["MIPGap"] = termination_gap
    opt.options["TimeLimit"] = hard_time_limit
    opt.set_callback(callback.callback)

    def solve_model(_model, weights, df, name):
        model = _model.clone()

        objectives_list = [model.c_max, model.flow_time, model.w_flow_time,
                           model.tardiness, model.w_tardiness,
                           model.tardy_jobs, model.w_tardy_jobs]

        if name == "Gantt":
            model.start_time = pyo.Var(domain=pyo.NonNegativeReals, doc="Summation of Start Times")

            def start_time_summation_constraint(mo):
                return model.start_time == sum(model.s_jt[j, f, t, mc] for (j, f, t, mc) in model.s_jt_index)

            model.start_time_summation_constraint = pyo.Constraint(rule=start_time_summation_constraint)

            objectives_list.append(model.start_time)
            weights.append(0)

        model.objective = pyo.Objective(rule=funcs.objective_function_weights(objectives_list, weights),
                                        sense=pyo.minimize, name=name)

        opt.set_instance(model)
        opt.solve(tee=True)
        writer = pd.ExcelWriter(os.path.join("Outputs", name + ".xlsx"))
        funcs.print_vars(writer, model.x, "jftmc", binary=True)
        funcs.print_vars(writer, model.c_j, "jf", binary=False)
        funcs.print_vars(writer, model.c_jt, "jftmc", binary=False)
        funcs.print_vars(writer, model.s_jt, "jftmc", binary=False)
        funcs.print_vars(writer, model.y, "ftmc", binary=True)
        writer.close()

        if name == "Gantt":
            gc.main(model)
        else:
            if df.empty:
                df = funcs.print_objectives(objectives_list, callback, name)
            else:
                df.loc[name] = funcs.print_objectives(objectives_list, callback, name)

        del model

        df.to_excel("Output Summary.xlsx")

        return df

    objs_df = pd.read_excel("Output Summary.xlsx", index_col=0, header=0)
    # objs_df = solve_model(m, [1, 0, 0, 0, 0, 0, 0], objs_df, "Max Completion Time")
    # objs_df = solve_model(m, [0, 1, 0, 0, 0, 0, 0], objs_df, "Flow Time")
    # objs_df = solve_model(m, [0, 0, 1, 0, 0, 0, 0], objs_df, "Weighted Flow Time")
    # objs_df = solve_model(m, [0, 0, 0, 1, 0, 0, 0], objs_df, "Total Tardiness")
    # objs_df = solve_model(m, [0, 0, 0, 0, 1, 0, 0], objs_df, "Total Weighted Tardiness")
    # objs_df = solve_model(m, [0, 0, 0, 0, 0, 10000, 0], objs_df, "Number of Tardy Jobs")
    # objs_df = solve_model(m, [0, 0, 0, 0, 0, 0, 1000], objs_df, "Weighted Number of Tardy Jobs")
    # objs_df = solve_model(m, [100 / 107, 100 / 802, 100 / 3538, 100 / 290, 100 / 909, 100 / 6, 100 / 22],
    #                       objs_df, "Evenly Weighted Model")
    objs_df = solve_model(m, [1, 0, 0, 0, 0, 0, 0], objs_df, "Gantt")

    objs_df.to_excel("Output Summary.xlsx")

    print(objs_df)
