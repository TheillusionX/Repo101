import pandas as pd
import pyomo.environ as pyo
import pyomo.opt as pyopt
import functions as f


def tardiness(m):
    return pyo.summation(m.T)


def weighted_tardiness(m):
    return pyo.summation(m.w, m.T)


def num_of_tardy_jobs(m):
    return pyo.summation(m.U)


def weighted_num_of_tardy_jobs(m):
    return pyo.summation(m.w, m.U)


def max_tardiness(m, j):
    return m.mT >= m.T[j]


def weighted_max_tardiness(m, j):
    return m.WmT >= m.w[j] * m.T[j]


def one_job_one_position(m, j):
    return sum(m.x[j, t] for t in m.t) == 1


def one_position_one_job(m, t):
    return sum(m.x[j, t] for j in m.J) == 1


def completion_time_of_position_t(m, j, t):
    if pyo.value(t) > 1:
        return m.Cjt[j, t] >= sum(m.Cjt[i, t - 1] for i in m.J) + m.p[j] * m.x[j, t] - bigM * (1 - m.x[j, t])
    else:
        return m.Cjt[j, t] >= m.p[j] * m.x[j, t] - bigM * (1 - m.x[j, t])


def completion_time_of_job_j(m, j):
    return m.C[j] == sum(m.Cjt[j, t] for t in m.t)


def tardiness_variable(m, j):
    return m.T[j] >= m.C[j] - m.d[j]


def lateness_variable(m, j):
    return bigM * m.U[j] + f.eps >= m.T[j]


def get_schedule(m):
    schedule = []
    for t in m.J:
        for j in m.J:
            if pyo.value(m.x[j, t]) > 1 - f.eps:
                schedule.append(j)
                continue
    return schedule


def main(relaxed=False, time_limit=10, focus=0, termination_gap=0, counter_limit=5, tolerance=1):
    data = pd.read_csv("data.csv", index_col=0)
    jobs = data.T
    global bigM
    bigM = jobs["due date"].max() * 2

    m = pyo.ConcreteModel(name="F1 Scheduling Model")
    m.J = pyo.Set(initialize=range(1, len(jobs) + 1), doc="Position index range, t, of jobs", name="Position of Jobs")
    m.t = pyo.Set(initialize=range(1, len(jobs) + 1), doc="Index range of jobs, j", name="Set of Jobs")

    m.x = pyo.Var(m.J, m.t, within=pyo.Binary if not relaxed else pyo.NonNegativeReals, bounds=[0, 1],
                  name="X(i, j)")
    m.Cjt = pyo.Var(m.J, m.t, within=pyo.NonNegativeReals, name="C(j, t)")
    m.C = pyo.Var(m.J, within=pyo.NonNegativeReals, name="C(j)")
    m.T = pyo.Var(m.J, within=pyo.NonNegativeReals, name="T(j)")
    m.U = pyo.Var(m.J, within=pyo.Binary if not relaxed else pyo.NonNegativeReals, bounds=[0, 1],
                  name="U(j)")
    m.mT = pyo.Var(within=pyo.NonNegativeReals)
    m.WmT = pyo.Var(within=pyo.NonNegativeReals)

    m.p = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "Proc. Time"])
    m.d = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "due date"])
    m.w = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "weight"])

    m.C1 = pyo.Constraint(m.J, rule=one_job_one_position)
    m.C2 = pyo.Constraint(m.t, rule=one_position_one_job)
    m.C3 = pyo.Constraint(m.J, m.t, rule=completion_time_of_position_t)
    m.C4 = pyo.Constraint(m.J, rule=completion_time_of_job_j)
    m.CT = pyo.Constraint(m.J, rule=tardiness_variable)
    m.CU = pyo.Constraint(m.J, rule=lateness_variable)

    m.mTC = pyo.Constraint(m.J, rule=max_tardiness)
    m.WmTC = pyo.Constraint(m.J, rule=weighted_max_tardiness)

    callback = f.CallbackFunction(time_limit=time_limit, counter_limit=counter_limit, tolerance=tolerance)
    opt = pyopt.SolverFactory('gurobi_persistent', solver_io="python")
    opt.options["MIPFocus"] = focus
    opt.options["MIPGap"] = termination_gap
    opt.set_callback(callback.callback)

    m.tardiness = pyo.Objective(rule=tardiness, sense=pyo.minimize, name="Tardiness")
    m.weighted_tardiness = pyo.Objective(rule=weighted_tardiness, sense=pyo.minimize, name="W-Tardiness")
    m.num_of_tardies = pyo.Objective(rule=num_of_tardy_jobs, sense=pyo.minimize, name="Tardy Jobs")
    m.weighted_num_of_tardies = pyo.Objective(rule=weighted_num_of_tardy_jobs, sense=pyo.minimize, name="W-Tardy Jobs")
    m.max_tardiness = pyo.Objective(rule=m.mT, sense=pyo.minimize, name="Max Tardiness")
    m.weighted_max_tardiness = pyo.Objective(rule=m.WmT, sense=pyo.minimize, name="W-Max Tardiness")

    m.tardiness.deactivate()
    m.weighted_tardiness.deactivate()
    m.num_of_tardies.deactivate()
    m.weighted_num_of_tardies.deactivate()
    m.max_tardiness.deactivate()
    m.weighted_max_tardiness.deactivate()

    file_name_prefix = "" if not relaxed else "Relaxed "
    file_name_root = "F1 Formulation.xlsx"
    file_name = file_name_prefix + file_name_root

    m2 = m.clone()

    # tardiness
    f.solve_and_print(m2, m2.tardiness, opt, "Outputs\\Tardiness", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)

    # weighted tardiness
    del m2
    m2 = m.clone()
    f.solve_and_print(m2, m2.weighted_tardiness, opt, "Outputs\\Weighted Tardiness", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)

    # num of tardy jobs
    del m2
    m2 = m.clone()
    f.solve_and_print(m2, m2.num_of_tardies, opt, "Outputs\\Tardy Jobs", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)

    # weighted num of tardy jobs
    del m2
    m2 = m.clone()
    f.solve_and_print(m2, m2.weighted_num_of_tardies, opt, "Outputs\\Weighted Tardy Jobs", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)

    # max tardiness
    del m2
    m2 = m.clone()
    f.solve_and_print(m2, m2.max_tardiness, opt, "Outputs\\Max Tardiness", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)

    # weighted max tardiness
    del m2
    m2 = m.clone()
    f.solve_and_print(m2, m2.weighted_max_tardiness, opt, "Outputs\\Weighted Max Tardiness", file_name, callback,
                      one_dims=[m2.C, m2.T, m2.U], two_dims=[m2.x, m2.Cjt],
                      schedule=get_schedule)
