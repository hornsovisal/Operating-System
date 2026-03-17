import threading
import time
import random

BUFFER_SIZE = 100
PAIR_COUNT_PER_PRODUCER = 10
NUM_PRODUCERS = 3

# Shared resources
buffer = []
buffer_lock = threading.Semaphore(1)      # mutex for buffer access
empty_slots = threading.Semaphore(BUFFER_SIZE)  # count empty particle slots
full_slots = threading.Semaphore(0)       # count filled particle slots

pair_id = 1
pair_id_lock = threading.Lock()


def get_next_pair_id():
    global pair_id
    with pair_id_lock:
        current = pair_id
        pair_id += 1
        return current


def producer_before(name):
    """
    WRONG / before semaphore:
    no synchronization, may overflow / mix operations logically
    """
    global buffer
    for _ in range(PAIR_COUNT_PER_PRODUCER):
        pid = get_next_pair_id()
        p1 = f"{pid}A"
        p2 = f"{pid}B"

        # no protection
        if len(buffer) + 2 <= BUFFER_SIZE:
            buffer.append(p1)
            time.sleep(random.uniform(0.001, 0.02))
            buffer.append(p2)
            print(f"[BEFORE] {name} produced pair ({p1}, {p2}) | buffer size = {len(buffer)}")
        else:
            print(f"[BEFORE] {name} could not safely insert pair ({p1}, {p2}) | buffer full-ish")

        time.sleep(random.uniform(0.01, 0.05))


def consumer_before():
    """
    WRONG / before semaphore:
    can try to consume when not enough particles
    """
    global buffer
    for _ in range(NUM_PRODUCERS * PAIR_COUNT_PER_PRODUCER):
        if len(buffer) >= 2:
            p1 = buffer.pop(0)
            time.sleep(random.uniform(0.001, 0.02))
            p2 = buffer.pop(0)
            print(f"[BEFORE] Consumer packed ({p1}, {p2}) | buffer size = {len(buffer)}")
        else:
            print("[BEFORE] Consumer ERROR: buffer does not have 2 particles!")

        time.sleep(random.uniform(0.01, 0.05))


def producer_after(name):
    """
    Correct version using semaphores
    Rules:
    - reserve 2 empty slots
    - lock buffer so pair is placed consecutively
    - signal 2 full slots
    """
    global buffer
    for _ in range(PAIR_COUNT_PER_PRODUCER):
        pid = get_next_pair_id()
        p1 = f"{pid}A"
        p2 = f"{pid}B"

        empty_slots.acquire()
        empty_slots.acquire()

        buffer_lock.acquire()
        buffer.append(p1)
        buffer.append(p2)
        print(f"[AFTER] {name} produced pair ({p1}, {p2}) | buffer size = {len(buffer)}")
        buffer_lock.release()

        full_slots.release()
        full_slots.release()

        time.sleep(random.uniform(0.01, 0.05))


def consumer_after():
    """
    Correct version using semaphores
    - wait until 2 particles exist
    - lock buffer while removing them
    - signal 2 empty slots
    """
    global buffer
    total_pairs = NUM_PRODUCERS * PAIR_COUNT_PER_PRODUCER

    for _ in range(total_pairs):
        full_slots.acquire()
        full_slots.acquire()

        buffer_lock.acquire()
        p1 = buffer.pop(0)
        p2 = buffer.pop(0)
        print(f"[AFTER] Consumer packed ({p1}, {p2}) | buffer size = {len(buffer)}")
        buffer_lock.release()

        empty_slots.release()
        empty_slots.release()

        time.sleep(random.uniform(0.01, 0.05))


def run_before():
    global buffer, pair_id
    buffer = []
    pair_id = 1

    print("\n=== PROBLEM 1: BEFORE SEMAPHORE ===\n")

    threads = []
    for i in range(NUM_PRODUCERS):
        t = threading.Thread(target=producer_before, args=(f"Producer-{i+1}",))
        threads.append(t)

    c = threading.Thread(target=consumer_before)
    threads.append(c)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n[BEFORE] Final buffer:", buffer)


def run_after():
    global buffer, pair_id, buffer_lock, empty_slots, full_slots
    buffer = []
    pair_id = 1

    buffer_lock = threading.Semaphore(1)
    empty_slots = threading.Semaphore(BUFFER_SIZE)
    full_slots = threading.Semaphore(0)

    print("\n=== PROBLEM 1: AFTER SEMAPHORE ===\n")

    threads = []
    for i in range(NUM_PRODUCERS):
        t = threading.Thread(target=producer_after, args=(f"Producer-{i+1}",))
        threads.append(t)

    c = threading.Thread(target=consumer_after)
    threads.append(c)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n[AFTER] Final buffer:", buffer)


if __name__ == "__main__":
    run_before()
    print("\n" + "=" * 70 + "\n")
    run_after()