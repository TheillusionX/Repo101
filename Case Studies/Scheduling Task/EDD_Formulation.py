import pandas as pd
import pyomo.environ as pyo
import pyomo.opt as pyopt
import functions as f


def main(relaxed=False, time_limit=10, focus=0, termination_gap=0, counter_limit=5, tolerance=1):
    data = pd.read_csv("data.csv", index_col=0)
    jobs = data.T
    global bigM
    bigM = jobs["due date"].max() * 2

    m = pyo.ConcreteModel(name="F1 Scheduling Model")
    m.J = pyo.Set(initialize=range(1, len(jobs) + 1), doc="Position index range, t, of jobs", name="Position of Jobs")
    m.t = pyo.Set(initialize=range(1, len(jobs) + 1), doc="Index range of jobs, j", name="Set of Jobs")

    m.p = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "Proc. Time"])
    m.d = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "due date"])
    m.w = pyo.Param(m.J, initialize=lambda m, x: jobs.loc[str(x), "weight"])

    m.x = pyo.Var(m.J, m.t, within=pyo.Binary if not relaxed else pyo.NonNegativeReals, bounds=[0, 1],
                  name="X(i, j)")

    jobs_order = sorted(list(m.J), key=lambda j: m.d[j])
    print(jobs_order)
    for j, t in zip(jobs_order, m.t):
        m.x[j, t].fix(1)

    m.Cj = pyo.Param(m.J, within=pyo.NonNegativeReals, name="C(j)",
                   initialize=lambda m, j: sum([m.p[x] for x in jobs_order[: jobs_order.index(j) + 1]]))
    m.T = pyo.Param(m.J, within=pyo.NonNegativeReals, name="T(j)",
                  initialize=lambda m, j: max(0, m.Cj[j] - m.d[j]))
    m.U = pyo.Param(m.J, within=pyo.Binary if not relaxed else pyo.NonNegativeReals,
                  name="U(j)",
                  initialize=lambda m, j: 1 if m.T[j] > f.eps else 0)
    m.mT = pyo.Param(within=pyo.NonNegativeReals,
                   initialize=max([m.T[j] for j in m.J]))
    m.WmT = pyo.Param(within=pyo.NonNegativeReals,
                   initialize=max([m.w[j]*m.T[j] for j in m.J]))

    callback = f.CallbackFunction(time_limit=time_limit, counter_limit=counter_limit, tolerance=tolerance)
    opt = pyopt.SolverFactory('gurobi_direct', solver_io="python")
    opt.options["MIPFocus"] = focus
    opt.options["MIPGap"] = termination_gap

    m.tardiness = pyo.Param(initialize=sum(m.T[j] for j in m.J), name="Tardiness")
    m.weighted_tardiness = pyo.Param(initialize=sum(m.w[j] * m.T[j] for j in m.J), name="W-Tardiness")
    m.num_of_tardies = pyo.Param(initialize=sum(m.U[j] for j in m.J), name="Tardy Jobs")
    m.weighted_num_of_tardies = pyo.Param(initialize=sum(m.w[j] * m.U[j] for j in m.J), name="W-Tardy Jobs")
    m.max_tardiness = pyo.Param(initialize=m.mT, name="Max Tardiness")
    m.weighted_max_tardiness = pyo.Param(initialize=m.WmT, name="W-Max Tardiness")

    file_name_prefix = "" if not relaxed else "Relaxed "
    file_name_root = "EDD Formulation.xlsx"
    file_name = file_name_prefix + file_name_root

    one_dims = [m.Cj, m.T, m.U]
    two_dims = [m.x]

    f.print_results("Outputs", file_name, m,
                    one_dims=one_dims, two_dims=two_dims,
                    callback_object=callback)
