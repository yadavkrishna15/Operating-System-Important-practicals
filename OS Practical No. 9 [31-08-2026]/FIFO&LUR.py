def fifo(pages, frames):
    memory = []
    hits = 0
    faults = 0
    pointer = 0

    print("\nFIFO Page Replacement")

    for page in pages:
        if page in memory:
            hits += 1
            print(page, "-> Hit  ", memory)
        else:
            faults += 1

            if len(memory) < frames:
                memory.append(page)
            else:
                memory[pointer] = page
                pointer = (pointer + 1) % frames

            print(page, "-> Miss ", memory)

    return hits, faults


def lru(pages, frames):
    memory = []
    hits = 0
    faults = 0

    print("\nLRU Page Replacement")

    for page in pages:
        if page in memory:
            hits += 1
            memory.remove(page)
            memory.append(page)
            print(page, "-> Hit  ", memory)
        else:
            faults += 1

            if len(memory) >= frames:
                memory.pop(0)

            memory.append(page)
            print(page, "-> Miss ", memory)

    return hits, faults


pages = list(map(int, input("Enter page reference string: ").split()))
frames = int(input("Enter number of frames: "))

total = len(pages)

fifo_hits, fifo_faults = fifo(pages, frames)

print("\nFIFO Results")
print("Page Hits:", fifo_hits)
print("Page Faults:", fifo_faults)
print("Hit Ratio:", fifo_hits / total)
print("Miss Ratio:", fifo_faults / total)

lru_hits, lru_faults = lru(pages, frames)

print("\nLRU Results")
print("Page Hits:", lru_hits)
print("Page Faults:", lru_faults)
print("Hit Ratio:", lru_hits / total)
print("Miss Ratio:", lru_faults / total)
