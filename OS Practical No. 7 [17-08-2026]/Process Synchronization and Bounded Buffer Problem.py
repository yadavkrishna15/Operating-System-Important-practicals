import threading
import time
import random

# Buffer size
BUFFER_SIZE = 5

# Shared buffer (Circular Queue)
buffer = [None] * BUFFER_SIZE
front = 0
rear = 0

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)  # Empty slots
full = threading.Semaphore(0)             # Filled slots
mutex = threading.Lock()                  # Mutual exclusion

# Producer Function
def producer():
    global rear

    for i in range(10):
        item = random.randint(1, 100)

        empty.acquire()      # Wait if buffer is full
        mutex.acquire()      # Enter critical section

        buffer[rear] = item
        print(f"Producer produced: {item}")
        rear = (rear + 1) % BUFFER_SIZE

        mutex.release()      # Exit critical section
        full.release()       # Signal that an item is available

        time.sleep(1)

# Consumer Function
def consumer():
    global front

    for i in range(10):
        full.acquire()       # Wait if buffer is empty
        mutex.acquire()      # Enter critical section

        item = buffer[front]
        print(f"Consumer consumed: {item}")
        buffer[front] = None
        front = (front + 1) % BUFFER_SIZE

        mutex.release()      # Exit critical section
        empty.release()      # Signal that a slot is free

        time.sleep(2)

# Create Threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start Threads
producer_thread.start()
consumer_thread.start()

# Wait for Completion
producer_thread.join()
consumer_thread.join()

print("\nExecution Completed!")
