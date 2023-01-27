from DijkstraAlgorithm import DijkstraSolver
from CriticalPath import CriticalPathSolver
import pandas as pd

pd.set_option('display.max_columns', 1000)

# how to use DijkstraSolver:
# 1- create object, use pandas dataframe as first argument, and origin and end node (as shown in csv file) as
# second and third node
#
# 2- use .solve() function
#
# 3- print object
task_1_data = pd.read_csv("Diagram_1.csv")
task_1 = DijkstraSolver(task_1_data, "s1", "s20")
task_1.solve()

print(task_1)

# how to use CriticalPathSolver:
# 1- create object, use pandas dataframe as argument, as shown
#
# 2- use .solve() function
#
# 3- print object
task_3_data = pd.read_csv("Diagram_3.csv", index_col = 0, na_values = [" "])
Task3 = CriticalPathSolver(task_3_data)
Task3.solve()

print(Task3)