from concurrent.futures import ThreadPoolExecutor
import threading

# Shared variable
completed_tasks = 0

# Lock for synchronization
lock = threading.Lock()

def fibonacci(n):
    global completed_tasks

    # Generate Fibonacci series
    a, b = 0, 1
    series = []

    for _ in range(n):
        series.append(str(a))
        a, b = b, a + b

    # Print safely
    with lock:
        completed_tasks += 1
        print("------------------------------------")
        print("Thread Name :", threading.current_thread().name)
        print("Number of Terms :", n)
        print("Fibonacci Series :", " ".join(series))
        print("Completed Tasks :", completed_tasks)
        print("------------------------------------")

def main():
    print("==========================================")
    print(" MULTI-THREADING AND FIBONACCI GENERATION ")
    print("==========================================")

    # Thread Pool
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(fibonacci, 5)
        executor.submit(fibonacci, 8)
        executor.submit(fibonacci, 10)

    print("\nAll Tasks Completed Successfully.")

if __name__ == "__main__":
    main()
print("KRISHNA YADAV S124")
