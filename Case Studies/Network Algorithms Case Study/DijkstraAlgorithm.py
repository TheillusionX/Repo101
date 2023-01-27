# Author: Youssef Nsouli
# ID: 2487494

import pandas as pd
MAX_VALUE = 2**63 - 1

class DijkstraSolver:
    def __init__(self, distances_table, origin, end):
        # initializing distance table with the right format, rows starting with node names
        distances_table = distances_table.set_axis(list(distances_table.columns), axis = 0)

        # turning data into integers, and m into 64-bit max integer value to signify inability to pass from node i to node j
        # to make computation easier
        for i in range(0, len(distances_table.index)):
            for j in range(0, len(distances_table.columns)):
                try:
                    distances_table.iloc[i, j] = int(distances_table.iloc[i, j])
                except:
                    if distances_table.iloc[i, j] == "m":
                        distances_table.iloc[i, j] = MAX_VALUE

        self.distances_table = distances_table
        self.origin = origin
        self.end = end
        self.solved = False

        # initialzing solution table, Dijkstra's table
        self.solution_table = pd.DataFrame(columns = self.distances_table.columns)

        # creates iteration 0, and the node that has a cell with a listo of three elements is a permanently labeled one
        self.solution_table.loc[len(self.solution_table.index)] = \
            [[self.origin, 0, "F"]] + [["-", MAX_VALUE]] * (len(self.solution_table.columns) - 1)

    def display(self):
        # to-be-returned string
        ret_str = ""
        # formatting header
        heading = "{:>9s} ".format("Nodes:")
        for i in self.solution_table.columns:
            heading += "{:^12s}".format(i.capitalize())
        ret_str += heading + "\n"

        # formatting rows
        for i in self.solution_table.index:
            row = "{:6s}{:2d}: ".format("Iter.", i)

            for j in self.solution_table.iloc[i]:
                row += "({:>3s}, {:>4s}) ".format(j[0].capitalize(), str("M" if j[1] == MAX_VALUE else j[1]) + ("/F" if len(j) == 3 else ""))

            ret_str += row + "\n"

        return ret_str

    def go_step(self, starter_node):
        # defining variables

        # from csv file
        distances_to_current_node = self.distances_table.loc[starter_node]

        # in order to look at distance from previous iteration
        previous_sol_iter = self.solution_table.iloc[len(self.solution_table.index) - 1]

        # distance written in the most recently permanently labeled node
        current_distance = self.solution_table.loc[len(self.solution_table.index) - 1, starter_node][1]

        # list in order to add it to solution_table
        current_iteration = []

        # iterates over all nodes
        # prev_sol will be a ('node', _distance_,) and dist is the distance from most recently permanently labeled node
        # to currently iterated node
        for (prev_sol, dist) in zip(previous_sol_iter, distances_to_current_node):
            if dist + current_distance < prev_sol[1] and len(prev_sol) == 2:
                current_iteration.append([starter_node, dist + current_distance])
            else:
                # [] + ... is to create a new reference for the list so any changes to the list, like append
                # or value modification won't affect previous iterations of where the list is used
                current_iteration.append(prev_sol.copy())

        # appends solution list
        self.solution_table.loc[len(self.solution_table.index)] = current_iteration

        # to check which node to permanently label
        distance_for_permanent_label_candidate = MAX_VALUE
        candidate_for_permanent_label = starter_node

        # iteration
        for i in range(0, len(current_iteration)):
            node = current_iteration[i]

            # checks if node is temporarily labeled and if the distance written is the shortest one yet
            if len(node) == 2 and node[1] < distance_for_permanent_label_candidate:
                distance_for_permanent_label_candidate = node[1]

                # gets the name of the node
                candidate_for_permanent_label = self.solution_table.columns[i]

        # appends an element to signify permanent label
        self.solution_table.loc[len(self.solution_table.index) - 1, candidate_for_permanent_label].append("F")

        # returns the most recently permanently labeled node
        return candidate_for_permanent_label

    def solve(self):
        if not self.solved:
            # initiation variable
            current_node = self.origin

            # repeats until end node is permanently labeled
            while len(self.solution_table.loc[len(self.solution_table.index) - 1, self.end]) != 3:
                current_node = self.go_step(current_node)

        # returns the shortest distance from origin to end
        return self.solution_table.loc[len(self.solution_table.index) - 1, self.end][1]

    # for print function compatibility
    def __str__(self):
        return self.display()


