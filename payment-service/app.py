from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s service=payment-service level=%(levelname)s message=%(message)s"
)

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "payment_service_requests_total",
    "Total requests received by Payment Service",
    ["endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "payment_service_request_latency_seconds",
    "Payment Service latency",
    ["endpoint"]
)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "payment-service"})

@app.route("/pay")
def pay():
    start = time.time()

    logging.info("Received payment request")

    time.sleep(random.uniform(0.1, 0.5))

    if random.random() < 0.2:
        logging.error("Payment failed with 500 error")

        REQUEST_COUNT.labels(endpoint="/pay", status=500).inc()
        REQUEST_LATENCY.labels(endpoint="/pay").observe(time.time() - start)

        return jsonify({"error": "Payment failed"}), 500

    logging.info("Payment successful")

    REQUEST_COUNT.labels(endpoint="/pay", status=200).inc()
    REQUEST_LATENCY.labels(endpoint="/pay").observe(time.time() - start)

    return jsonify({"status": "payment successful"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)