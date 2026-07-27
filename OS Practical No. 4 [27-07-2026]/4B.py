print("S124 KRISHNA YADAV")

processes = [
    ["P1", 0, 7],
    ["P2", 2, 4],
    ["P3", 4, 1],
    ["P4", 5, 4]
]

n = len(processes)
completed = []
current_time = 0
total_wt = 0
total_tat = 0
gantt = []

# Calculate Waiting Time and Turnaround Time
while len(completed) < n:
    available = []

    for p in processes:
        if p not in completed and p[1] <= current_time:
            available.append(p)

    if not available:
        current_time += 1
        continue

    available.sort(key=lambda x: x[2])

    p = available[0]
    name, at, bt = p

    wt = current_time - at
    tat = wt + bt

    total_wt += wt
    total_tat += tat

    gantt.append((name, current_time, current_time + bt))

    current_time += bt
    completed.append(p)

# Display Result
print("Process\tAT\tBT\tWT\tTAT")

current_time = 0
completed = []

while len(completed) < n:
    available = []

    for p in processes:
        if p not in completed and p[1] <= current_time:
            available.append(p)

    if not available:
        current_time += 1
        continue

    available.sort(key=lambda x: x[2])

    p = available[0]
    name, at, bt = p

    wt = current_time - at
    tat = wt + bt

    print(f"{name}\t{at}\t{bt}\t{wt}\t{tat}")

    current_time += bt
    completed.append(p)

print("\nAverage Waiting Time =", total_wt / n)
print("Average Turnaround Time =", total_tat / n)

print("\nGantt Chart")

for g in gantt:
    print(f"| {g[0]} ", end="")
print("|")

print(gantt[0][1], end="")

for g in gantt:
    print(f" {g[2]}", end="")

print()
