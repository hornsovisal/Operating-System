import threading
import time
import random

# -----------------------------
# BEFORE SEMAPHORE
# -----------------------------
output_before = []


def process1_before():
    output_before.append("H")
    time.sleep(random.uniform(0.001, 0.02))
    output_before.append("E")


def process2_before():
    time.sleep(random.uniform(0.001, 0.02))
    output_before.append("L")


def process3_before():
    time.sleep(random.uniform(0.001, 0.02))
    output_before.append("O")


# -----------------------------
# AFTER SEMAPHORE
# Want exactly: HELLO once
# Process 1 prints H and E
# Process 2 prints L twice
# Process 3 prints O once
# -----------------------------
output_after = []

a = threading.Semaphore(1)  # allow Process 1 to start
b = threading.Semaphore(0)  # Process 2 waits
c = threading.Semaphore(0)  # Process 3 waits


def process1_after():
    a.acquire()
    output_after.append("H")
    time.sleep(random.uniform(0.001, 0.02))
    output_after.append("E")
    b.release()


def process2_after():
    b.acquire()
    output_after.append("L")
    time.sleep(random.uniform(0.001, 0.02))
    output_after.append("L")
    c.release()


def process3_after():
    c.acquire()
    output_after.append("O")


def run_before():
    global output_before
    output_before = []

    print("=== PROBLEM 2: BEFORE SEMAPHORE ===")

    t1 = threading.Thread(target=process1_before)
    t2 = threading.Thread(target=process2_before)
    t3 = threading.Thread(target=process3_before)

    threads = [t1, t2, t3]
    random.shuffle(threads)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    result = "".join(output_before)
    print("[BEFORE] Output:", result)


def run_after():
    global output_after, a, b, c
    output_after = []

    a = threading.Semaphore(1)
    b = threading.Semaphore(0)
    c = threading.Semaphore(0)

    print("\n=== PROBLEM 2: AFTER SEMAPHORE ===")

    t1 = threading.Thread(target=process1_after)
    t2 = threading.Thread(target=process2_after)
    t3 = threading.Thread(target=process3_after)

    threads = [t1, t2, t3]
    random.shuffle(threads)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    result = "".join(output_after)
    print("[AFTER] Output:", result)


if __name__ == "__main__":
    run_before()
    print()
    run_after()