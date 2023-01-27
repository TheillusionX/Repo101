"""
IE361 Case Study - Group 12
Abderrahmane Harkat     2415297
Alperen Oktay Şahin     2305373
Youssef Nsouli          2487494

Author: Youssef Nsouli
"""

import pyomo.environ as pyo

model = pyo.ConcreteModel(name = "Airline Optimal Pricing Policy")

# set of price level j
# model.j = pyo.Set(dimen = 1, initialize = range(1, 36 + 1))

# set of price level domains
model.d = pyo.Set(dimen = 1, initialize = range(1, 5 + 1), doc = "Price Level Domains, defined for a set {1, 2,... 8}.")

# set of price level ranges
model.r = pyo.Set(dimen = 1, initialize = range(1, 4 + 1), doc = "Price Level Ranges, defined for a set {1, 2,... 7}.")

# domain variable, z(d)
model.z = pyo.Var(model.d, bounds = (0, 1), initialize = 0,
                  doc = r"Domain Variable, z(d), that defines the linear interpolation that defines the value of the optimal price level, j.")

# range variables, y(r)
model.y = pyo.Var(model.r, domain = pyo.Binary, initialize = 0,
                  doc = r"Range Variable, y(r), that shows in which range interval the optimal price level, j, lies in.")

# price level, j
model.j = pyo.Var(bounds = (1, 36), within = pyo.NonNegativeIntegers, initialize = 1,
                  doc = "The price level, which determines the actual price.")

# expected demand value definition
def expected_demand(j):
    pj = 20 * j
    if 1 <= j <= 10:
        return 90 - (pj - 20)/20
    elif 11 <= j <= 20:
        return 80 - (pj - 220)/10
    elif 21 <= j <= 30:
        return 60 - 3 * (pj - 420)/20
    elif 31 <= j <= 36:
        return 30 - (pj - 620)/5
    else:
        return None

# Objective Function
def revenue_calculation(m):
    return m.j * (expected_demand(1) * m.z[1]
                  + expected_demand(11) * m.z[2]
                  + expected_demand(21) * m.z[3]
                  + expected_demand(31) * m.z[4]
                  + expected_demand(36) * m.z[5]) * 20

model.revenue = pyo.Objective(rule = revenue_calculation, sense = pyo.maximize,
                              doc = "Objective function, whose goal is to find the maximum expected attainable revenue")

# Constraints:
# All z(d) must sum to 1
model.linear_interpolation_constraint = \
    pyo.Constraint(rule = (sum(model.z[d] for d in model.d) == 1),
                   doc = r"Makes sure the domain variables, z(d), all sum to 1, strictly.")

# j is contained in one range interval
model.range_constraint = \
    pyo.Constraint(rule = (sum(model.y[r] for r in model.r) == 1),
                   doc = r"Makes sure only one range variable, y(r), is chosen.")


# z takes a value if j is in the range bounded by z
def range_bound_relation(m, i):
    if 1 < i < m.d.at(-1):
        return m.z[i] <= m.y[i] + m.y[i - 1]
    elif i == 1:
        return m.z[i] <= m.y[i]
    elif i == m.d.at(-1):
        return m.z[i] <= m.y[i - 1]

model.range_bound_relation_constraint = \
    pyo.Constraint(model.d, rule = range_bound_relation,
                   doc = r"Relation between the domain and range variables, z(d) and y(r), respectively.")

# the value of j is controlled by the value of the z variables
model.j_to_z = pyo.Constraint(rule = (model.j ==
                                      model.z[1]
                                      + 11 * model.z[2]
                                      + 21 * model.z[3]
                                      + 31 * model.z[4]
                                      + 36 * model.z[5]),
                              doc = "The price level is determined by the domain variables, z(d)")

solver = pyo.SolverFactory("ipopt", executable = "Ipopt_Package/bin/ipopt.exe")
results = solver.solve(model, tee = True)
model.pprint(verbose = True)
model.revenue.pprint()
