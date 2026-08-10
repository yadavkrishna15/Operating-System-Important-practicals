class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.rem = bt
        self.ct = 0
        self.tat = 0
        self.wt = 0


def print_result(title, procs):
    print(f"\n--- {title} ---")
    print("PID\tAT\tBT\tCT\tTAT\tWT")
    total_tat = total_wt = 0
    for p in procs:
        print(f"P{p.pid}\t{p.at}\t{p.bt}\t{p.ct}\t{p.tat}\t{p.wt}")
        total_tat += p.tat
        total_wt += p.wt
    n = len(procs)
    print(f"Average TAT = {total_tat / n:.2f} ms")
    print(f"Average WT  = {total_wt / n:.2f} ms")


def fcfs(procs):
    time = 0
    for p in procs:
        if time < p.at:
            time = p.at
        time += p.bt
        p.ct = time
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt
    print_result("FCFS", procs)


def round_robin(procs, quantum):
    n = len(procs)
    queue = []
    arrived = [False] * n
    time = 0
    done = 0

    # enqueue processes already arrived at time 0
    for i, p in enumerate(procs):
        if p.at <= time and not arrived[i]:
            queue.append(i)
            arrived[i] = True

    while done < n:
        if not queue:
            # jump to the next process that hasn't arrived yet
            next_i = min((i for i in range(n) if not arrived[i]), key=lambda i: procs[i].at)
            time = procs[next_i].at
            queue.append(next_i)
            arrived[next_i] = True
            continue

        idx = queue.pop(0)
        p = procs[idx]

        slice_time = min(p.rem, quantum)
        time += slice_time
        p.rem -= slice_time

        for i, q in enumerate(procs):
            if q.at <= time and not arrived[i]:
                queue.append(i)
                arrived[i] = True

        if p.rem > 0:
            queue.append(idx)
        else:
            p.ct = time
            p.tat = p.ct - p.at
            p.wt = p.tat - p.bt
            done += 1

    print_result(f"Round Robin (Quantum = {quantum} ms)", procs)


if __name__ == "__main__":
    quantum = 2

    p1 = [Process(1, 0, 5), Process(2, 1, 3), Process(3, 2, 6)]

    round_robin(p1, quantum)
