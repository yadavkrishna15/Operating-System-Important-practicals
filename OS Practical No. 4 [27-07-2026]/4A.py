# FCFS Scheduling Algorithm

print("S124 KRISHNA YADAV")

processes = [
    ["P1", 0, 5],
    ["P2", 1, 3],
    ["P3", 2, 8],
    ["P4", 3, 6]
]

# Sort by Arrival Time
processes.sort(key=lambda x: x[1])

current_time = 0
total_wt = 0
total_tat = 0
gantt = []

print("Process\tAT\tBT\tWT\tTAT")

for p in processes:
    name, at, bt = p

    if current_time < at:
        current_time = at

    wt = current_time - at
    tat = wt + bt

    total_wt += wt
    total_tat += tat

    gantt.append((name, current_time, current_time + bt))

    current_time += bt

    print(f"{name}\t{at}\t{bt}\t{wt}\t{tat}")

n = len(processes)

print("\nAverage Waiting Time =", total_wt / n)
print("Average Turnaround Time =", total_tat / n)

print("\nGantt Chart")

for g in gantt:
    print(f"| {g[0]} ", end="")
print("|")

print(gantt[0][1], end="")

for g in gantt:
    print(f"    {g[2]}", end="")

print()
