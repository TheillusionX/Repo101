# Author: Youssef Nsouli
# ID: 2487494

import pandas as pd
MAX_VALUE = 2**64 - 1

class CriticalPathSolver:
    def __init__(self, table):

        # gets data table and initializes it
        for i in range(0, len(table.iloc[:, 0])):

            # cleans NaN values
            table.fillna("", inplace = True)

            # puts predecessors in lists for iteration purposes
            if "-" in table.iloc[i, 0]:
                predecessor_list = table.iloc[i, 0].split("-")
                table.iloc[i, 0] = [predecessor_list[0]]

                for j in predecessor_list[1:]:
                    table.iloc[i, 0].append(j)
            elif len(table.iloc[i, 0]) == 1:
                table.iloc[i, 0] = [table.iloc[i, 0][0]]

        # initializes end time as 64-bit integer limit
        self.project_end_time = MAX_VALUE
        self.end_time_found = False
        self.table = table

        # initializes slack table
        self.slack_table = pd.DataFrame(index = self.table.index, columns = ["Total Slack", "Free Slack"])
        self.slack_table.fillna(0, inplace = True)

        # initializes table which identifies critical activities from non-criticals
        self.critical_act_table = pd.DataFrame(index = self.table.index, columns = ["Critical (Y/N)"])
        self.critical_act_table.fillna("", inplace = True)

        # initializes critical path solution table
        self.solution_table = pd.DataFrame(index = self.table.index, columns = ["Earliest Start", "Earliest Finish",
                                                                                "Latest Start", "Latest Finish"])
        self.solution_table.fillna(0, inplace = True)

    def forward_pass(self):
        # iterates over activities in index
        for i in range(0, len(self.solution_table.index)):

            # checks if activity has predecessors, if not, the start time is 0, and the end time is the duration
            if self.table.iloc[i, 0] == "":
                self.solution_table.iloc[i, 0] = 0
                self.solution_table.iloc[i, 1] = self.table.iloc[i, 1]

            # if activity has predecessors, all the earliest finish times are grouped in predessor_start_times
            # and the maximum is put as start time
            else:
                predecessor_start_times = []
                for predecessor in self.table.iloc[i, 0]:
                    predecessor_start_times.append(self.solution_table.loc[predecessor, "Earliest Finish"])
                self.solution_table.iloc[i, 0] = max(predecessor_start_times)
                self.solution_table.iloc[i, 1] = self.solution_table.iloc[i, 0] + self.table.iloc[i, 1]

        # grabs last finish time
        self.project_end_time = max(self.solution_table.iloc[:, 1])
        self.end_time_found = True

        return self.project_end_time

    def backward_pass(self):
        # backward pass needs end time as start time
        if self.end_time_found:

            # iterates over activities from the last activity to first
            for i in range(0, len(self.solution_table.index))[::-1]:
                current_activity = self.solution_table.index[i]

                # puts latest finish time of last activity as project end time
                self.solution_table.iloc[i, 3] = self.project_end_time

                successors_start_times = []

                # iterates over all predecessors, if the activity at hand is found as a predecessor,
                # the successor is stored, and their latest start time is stored in successors_start_time
                # the latest finish of activity at hand is the minimum of all latest start times
                for j in range(0, len(self.table.index)):
                    if current_activity in self.table.iloc[j, 0]:
                        successor = self.table.index[j]
                        successors_start_times.append(self.solution_table.loc[successor, "Latest Start"])

                        self.solution_table.iloc[i, 3] = min(successors_start_times)
                # calculates latest start time according to latest finish time
                self.solution_table.iloc[i, 2] = self.solution_table.iloc[i, 3] - self.table.iloc[i, 1]

            return self.project_end_time

        # if forward pass is not done, do forward pass before backward pass
        else:
            self.forward_pass()
            self.backward_pass()

    def get_slack(self):

        # iterates over activities
        for i in range(0, len(self.solution_table.index)):

            # gets and stores LF and EF and calculates total slack
            latest_finish_time = self.solution_table.iloc[i, 3]
            earliest_finish_time = self.solution_table.iloc[i, 1]
            self.slack_table.iloc[i, 0] = latest_finish_time - earliest_finish_time

            current_activity = self.solution_table.index[i]
            successors_start_times = []

            # gets successors start times and stores them in successors_start_times
            for j in range(0, len(self.table.index)):
                if current_activity in self.table.iloc[j, 0]:
                    successor = self.table.index[j]
                    successors_start_times.append(self.solution_table.loc[successor, "Earliest Start"])

            # if activity has successors, calculates free slack
            if len(successors_start_times) > 0:
                self.slack_table.iloc[i, 1] = min(successors_start_times) - earliest_finish_time

            # else, free slack is project end time - EF
            elif len(successors_start_times) == 0:
                self.slack_table.iloc[i, 1] = self.project_end_time - earliest_finish_time


        return self.slack_table


    def get_critical_activities(self):
        # makes sure that slack data is available
        self.get_slack()

        # if free slack is 0, then critical, otherwise its not critical
        for i in range(0, len(self.slack_table.index)):
            if self.slack_table.iloc[i, 0] == 0:
                self.critical_act_table.iloc[i, 0] = "Critical"
            else:
                self.critical_act_table.iloc[i, 0] = "-"

        return self.critical_act_table

    def solve(self):
        self.forward_pass()
        self.backward_pass()
        self.get_slack()

        return self.project_end_time

    # not related to algorithm
    def load_times_to_csv(self, file):
        self.solution_table.to_csv(file)

    def __str__(self):
        # to be used for print statements
        tempo_df = self.solution_table.copy()
        tempo_df[self.slack_table.columns[0]] = self.slack_table.iloc[:, 0]
        tempo_df[self.slack_table.columns[1]] = self.slack_table.iloc[:, 1]

        return str(tempo_df)