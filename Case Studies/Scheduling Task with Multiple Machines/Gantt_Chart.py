import matplotlib.pyplot as plt
import numpy as np
import pyomo.environ as pyo


def main(model):
    machines = list(model.mc)
    jobs = list(range(1, 15 + 1))

    job_color_map = np.random.rand(len(jobs), 3)

    start_times = np.array([[0] * len(jobs)] * len(machines))
    durations = np.array([[0] * len(jobs)] * len(machines))

    print(start_times)
    print(durations)

    for (j, f, t, m) in model.c_jt_index:
        if pyo.value(model.s_jt[j, f, t, m]) > 1e-2:
            start_times[m - 1, j - 1] = (pyo.value(model.s_jt[j, f, t, m]) -
                                         model.SC[m] * model.P_minor[j, f] -
                                         sum([model.SC[m] * model.P_major[f, g] * pyo.value(model.y[g, t, m])
                                              for g in model.f]))
        if pyo.value(model.c_jt[j, f, t, m]) > 1e-2:
            durations[m - 1, j - 1] = pyo.value(model.c_jt[j, f, t, m]) - start_times[m - 1, j - 1]

    print(start_times)
    print(durations)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(0, len(machines)):
        for j, f in model.jf:
            if durations[i, j - 1] > 1e-2:
                ax.barh(i + 1, durations[i, j - 1], left=start_times[i, j - 1], color=job_color_map[j - 1])
                ax.text(s=f"({j},{f})", y=i + 1, x=start_times[i, j - 1] + durations[i, j - 1] / 2,
                        ha="center", va="center")

    # Customize chart
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.set_title('Flowshop Schedule Gantt Chart')
    plt.savefig("Flowshop Schedule Gantt.png")
