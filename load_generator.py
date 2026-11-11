
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

import requests

URL = "http://localhost:5001/orders"
TARGET_QPS = 100
MAX_WORKERS = 150
DURATION_SECONDS = 0  # 0 = run continuously

results = Counter()
lock = threading.Lock()
session = requests.Session()


def send_request():
    try:
        response = session.get(URL, timeout=5)
        status = response.status_code
    except requests.RequestException:
        status = "connection_error"

    with lock:
        results[status] += 1


def main():
    print(f"Starting load test: {TARGET_QPS} QPS")
    print("Press Ctrl+C to stop\n")

    start = time.monotonic()
    next_request = start
    sent = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        try:
            while True:
                now = time.monotonic()

                if DURATION_SECONDS and now - start >= DURATION_SECONDS:
                    break

                if now < next_request:
                    time.sleep(next_request - now)

                executor.submit(send_request)
                sent += 1
                next_request = start + sent / TARGET_QPS

                if sent % TARGET_QPS == 0:
                    with lock:
                        snapshot = dict(results)
                    print(
                        f"Submitted: {sent} | "
                        f"Responses: {sum(snapshot.values())} | "
                        f"Status: {snapshot}"
                    )

        except KeyboardInterrupt:
            print("\nStopping traffic generator...")

    print("Final results:", dict(results))


if __name__ == "__main__":
    main()
