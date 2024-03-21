import pyomo.environ as pyo
import pandas as pd
import os
import datetime
from gurobipy import GRB

eps = 1e-4


def get_j_set(m, family):
    return pyo.Set(initialize=[(j, f) for f in family for j in m.j[f]])


def get_t_set(m, machines):
    return pyo.Set(initialize=[(t, mc) for mc in machines for t in m.t[mc]])


def get_job_data(m, data, col, three_d=False):
    if not three_d:
        return {(j, f): data[data["Type"] == f].loc[j, col] for f in m.f for j in m.j[f]}
    else:
        return {(j, f, mc): data[data["Type"] == f].loc[j, col] * m.RC[mc]
                for f in m.f for j in m.j[f] for mc in m.mc}


def objective_function_weights(objective_funcs_list, weights_list):
    for i, weight in enumerate(weights_list):
        if weight == 0:
            weights_list[i] = 1e-2
        weights_list[i] *= 100

    obj = 0
    for i, (weight, objective) in enumerate(zip(weights_list, objective_funcs_list)):
        obj += weight * objective

    return obj


def print_vars(writer, var, index_type, binary=False):
    vals = var.extract_values()

    if index_type == "jftmc":
        index = [(j, f) for (j, f, _, _) in vals.keys()]
        index = list(set(index))
        index = pd.MultiIndex.from_tuples(index, names=["Job", "Family"])

        cols = [(mc, t) for (_, _, t, mc) in vals.keys()]
        cols = list(set(cols))
        cols = pd.MultiIndex.from_tuples(cols, names=["Machine", "Position"])

        df = pd.DataFrame(index=index, columns=cols)
        df.sort_index(inplace=True)
        df.sort_index(inplace=True, axis=1)

        for j, f in df.index:
            for mc, t in df.columns:
                if binary:
                    df.loc[(j, f), (mc, t)] = 1 if int(round(vals[(j, f, t, mc)], 2)) == 1 else ""
                else:
                    df.loc[(j, f), (mc, t)] = round(vals[(j, f, t, mc)], 2) if (
                            round(vals[(j, f, t, mc)], 2) > eps) else ""

    elif index_type == "jf":
        index = [(j, f) for (j, f) in vals.keys()]
        index = list(set(index))
        index = pd.MultiIndex.from_tuples(index, names=["Job", "Family"])

        df = pd.DataFrame(index=index, columns=["Value"])
        df.sort_index(inplace=True)

        for j, f in df.index:
            df.loc[(j, f), "Value"] = round(vals[(j, f)], 2) if (round(vals[(j, f)], 2) > eps) else ""

    elif index_type == "ftmc":
        index = [f for (f, _, _) in vals.keys()]
        index = list(set(index))

        cols = [(mc, t) for (_, t, mc) in vals.keys()]
        cols = list(set(cols))
        cols = pd.MultiIndex.from_tuples(cols, names=["Machine", "Position"])

        df = pd.DataFrame(index=index, columns=cols)
        df.sort_index(inplace=True)
        df.sort_index(inplace=True, axis=1)

        for f in df.index:
            for mc, t in df.columns:
                if binary:
                    df.loc[f, (mc, t)] = 1 if int(round(vals[(f, t, mc)], 2)) == 1 else ""
                else:
                    df.loc[f, (mc, t)] = round(vals[(f, t, mc)], 2) if (
                            round(vals[(f, t, mc)], 2) > eps) else ""
    print(df)
    df.to_excel(writer, sheet_name=var.doc, index=True)


def print_objectives(objective_list, callback_object, name):
    other_objs_dct = {obj.doc: pyo.value(obj) for obj in objective_list}

    other_objs_dct["Time Taken"] = callback_object.time_taken if callback_object.time_taken > 1 else (
        (datetime.datetime.now() - callback_object.time).seconds)

    other_objs_dct["Node Count"] = callback_object.node_count

    return other_objs_dct


class CallbackFunction:
    best_obj = float("inf")
    time_since_best = 0
    time_limit = 0
    internal_counter = 0
    counter_limit = 0
    best_bound = float("inf")
    tolerance = 0
    time_taken = 0
    node_count = 0
    time = datetime.datetime.now()
    terminated = False

    def __init__(self, time_limit, counter_limit=5, tolerance=1):
        self.time_limit = time_limit
        self.counter_limit = counter_limit
        self.tolerance = tolerance

    def callback(self, cb_m, cb_opt, cb_where):
        if cb_where == 5:
            # Get model objective
            obj = cb_opt.cbGet(GRB.Callback.MIPNODE_OBJBST)
            best_bd = cb_opt.cbGet(GRB.Callback.MIPNODE_OBJBND)

            # Has objective changed?
            if abs(obj - self.best_obj) > self.tolerance or abs(best_bd - self.best_bound) > self.tolerance:
                # If so, update incumbent and time
                self.best_obj = obj
                self.best_bound = best_bd
                self.time_since_best = datetime.datetime.now()
                self.internal_counter = 0
            else:
                self.internal_counter += 1

            self.node_count = cb_opt.cbGet(GRB.Callback.MIPNODE_NODCNT)

            # Terminate if objective has not improved in 20s
            if ((datetime.datetime.now() - self.time_since_best).seconds > self.time_limit and
                    self.internal_counter > self.counter_limit):
                self.terminated = True
                cb_opt._solver_model.terminate()

    def exit(self, cb_opt):
        if self.terminated:
            self.time_taken = (datetime.datetime.now() - self.time).seconds - self.time_limit
        else:
            self.time_taken = (datetime.datetime.now() - self.time).seconds

    def reset(self):
        self.time_since_best = 0
        self.best_obj = float("inf")
        self.best_bound = float("inf")
        self.time_taken = 0
        self.node_count = 0
        self.internal_counter = 0
        self.time = datetime.datetime.now()
        self.terminated = False
