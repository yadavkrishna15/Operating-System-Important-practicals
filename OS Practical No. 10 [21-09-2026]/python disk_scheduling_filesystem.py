import random

# ==========================================
# PART 1: DISK SCHEDULING SIMULATION
# ==========================================

class DiskScheduler:
    def __init__(self, requests, initial_head, max_track=199):
        self.requests = list(requests)
        self.initial_head = initial_head
        self.max_track = max_track

    def fcfs(self):
        head = self.initial_head
        seek_count = 0
        sequence = [head]
        for req in self.requests:
            seek_count += abs(req - head)
            head = req
            sequence.append(head)
        return seek_count, sequence

    def sstf(self):
        head = self.initial_head
        pending = list(self.requests)
        seek_count = 0
        sequence = [head]
        while pending:
            closest = min(pending, key=lambda x: abs(x - head))
            seek_count += abs(closest - head)
            head = closest
            sequence.append(head)
            pending.remove(closest)
        return seek_count, sequence

    def c_scan(self):
        head = self.initial_head
        seek_count = 0
        sequence = [head]
        left = sorted([r for r in self.requests if r < head])
        right = sorted([r for r in self.requests if r >= head])
        
        current = head
        for r in right:
            seek_count += abs(r - current)
            current = r
            sequence.append(current)
        if left:
            seek_count += abs(self.max_track - current) + self.max_track
            sequence.append(self.max_track)
            sequence.append(0)
            current = 0
            for r in left:
                seek_count += abs(r - current)
                current = r
                sequence.append(current)
        return seek_count, sequence

    def c_look(self):
        head = self.initial_head
        seek_count = 0
        sequence = [head]
        left = sorted([r for r in self.requests if r < head])
        right = sorted([r for r in self.requests if r >= head])
        
        current = head
        for r in right:
            seek_count += abs(r - current)
            current = r
            sequence.append(current)
        if left:
            if right:
                seek_count += abs(right[-1] - left[0])
            current = left[0]
            for r in left:
                seek_count += abs(r - current)
                current = r
                sequence.append(current)
        return seek_count, sequence

    def rss(self):
        head = self.initial_head
        pending = list(self.requests)
        seek_count = 0
        sequence = [head]
        random.seed(42)
        while pending:
            chosen = random.choice(pending)
            seek_count += abs(chosen - head)
            head = chosen
            sequence.append(head)
            pending.remove(chosen)
        return seek_count, sequence


# ==========================================
# PART 2: SIMPLE FILE SYSTEM DESIGN
# ==========================================

class SimpleFileSystem:
    def __init__(self, total_blocks=20):
        self.total_blocks = total_blocks
        self.free_blocks = set(range(total_blocks))
        self.directory = {}

    def create_file(self, filename, data):
        print(f"\n[STEP] Attempting to create file: '{filename}'")
        if filename in self.directory:
            print(f"  -> Error: File '{filename}' already exists.")
            return False
        
        block_size = 10
        num_blocks = (len(data) + block_size - 1) // block_size
        print(f"  -> File size: {len(data)} bytes. Required blocks: {num_blocks} (1 block = 10 bytes)")
        
        if len(self.free_blocks) < num_blocks:
            print(f"  -> Error: Not enough free blocks!")
            return False
        
        allocated_blocks = []
        for _ in range(num_blocks):
            block = sorted(list(self.free_blocks))[0] # Allocate lowest available block
            self.free_blocks.remove(block)
            allocated_blocks.append(block)
            
        self.directory[filename] = {
            'blocks': allocated_blocks,
            'size': len(data),
            'data': data
        }
        print(f"  -> Success: Allocated physical blocks {allocated_blocks} to '{filename}'.")
        print(f"  -> Remaining Free Blocks: {sorted(list(self.free_blocks))}")
        return True

    def read_file(self, filename):
        print(f"\n[STEP] Attempting to read file: '{filename}'")
        if filename not in self.directory:
            print(f"  -> Error: File '{filename}' not found in directory.")
            return None
        
        file_info = self.directory[filename]
        print(f"  -> Directory Lookup Successful.")
        print(f"  -> Mapped Blocks: {file_info['blocks']}")
        print(f"  -> Retrieved Data: \"{file_info['data']}\"")
        return file_info['data']

    def delete_file(self, filename):
        print(f"\n[STEP] Attempting to delete file: '{filename}'")
        if filename not in self.directory:
            print(f"  -> Error: File '{filename}' not found.")
            return False
        
        file_info = self.directory[filename]
        freed_blocks = file_info['blocks']
        for block in freed_blocks:
            self.free_blocks.add(block)
            
        del self.directory[filename]
        print(f"  -> Success: Removed '{filename}' from directory.")
        print(f"  -> Freed blocks {freed_blocks} returned to free list.")
        print(f"  -> Current Free Blocks: {sorted(list(self.free_blocks))}")
        return True


# ==========================================
# MAIN EXECUTION WITH DETAILED STEPS
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print("=== 1.  DISK SCHEDULING SIMULATION ===")
    print("==================================================")
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    initial_head = 53
    
    ds = DiskScheduler(requests, initial_head)
    print(f"Initial Head Position: {initial_head}")
    print(f"Pending Requests Queue: {requests}\n")
    
    for algo_name, func in [("FCFS", ds.fcfs), ("SSTF", ds.sstf), ("C-SCAN", ds.c_scan), ("C-LOOK", ds.c_look), ("RSS", ds.rss)]:
        seek, seq = func()
        print(f"Algorithm: {algo_name}")
        print(f"  -> Movement Path: {seq}")
        print(f"  -> Total Seek Distance: {seek}\n")
    
    print("==================================================")
    print("=== 2.  FILE SYSTEM SIMULATION ===")
    print("==================================================")
    fs = SimpleFileSystem(total_blocks=10)
    
    # Step-by-step file operations
    fs.create_file("report.txt", "OS Lab Assignment.")
    fs.create_file("data.csv", "1,Rahul,A\n2,Aman,B")
    
    fs.read_file("report.txt")
    
    fs.delete_file("report.txt")
    
    fs.read_file("report.txt") # Will fail and show step error
