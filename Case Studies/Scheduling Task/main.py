import F1_Formulation as F1
import F2_Formulation as F2
import EDD_Formulation as EDD
import functions as f


time_limit = 30
counter_limit = 10
tolerance = 0.5
focus = 0
relaxed = False

F1.main(time_limit=time_limit, counter_limit=counter_limit, tolerance=tolerance, focus=focus, relaxed=relaxed)
F2.main(time_limit=time_limit, counter_limit=counter_limit, tolerance=tolerance, focus=focus, relaxed=relaxed)
EDD.main(time_limit=time_limit, counter_limit=counter_limit,tolerance=tolerance, focus=focus, relaxed=False)
f.summarize_results("Outputs", "Output Summary.xlsx")
