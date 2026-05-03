from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time
import random
import requests

app = Flask(__name__)

REQUEST_COUNT = Counter("order_service_requests_total", "Total requests received by Order Service", ["endpoint", "status"])
REQUEST_LATENCY = Histogram("order_service_request_latency_seconds", "Order Service request latency", ["endpoint"])

@app.route("/")
def home():
    return "Order Service is running"

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "order-service"})

@app.route("/orders")
def orders():
    start = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.4))

        payment_response = requests.get("http://payment-service:5000/pay", timeout=2)

        if payment_response.status_code != 200:
            REQUEST_COUNT.labels(endpoint="/orders", status=500).inc()
            REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)
            return jsonify({
                "error": "Order failed because payment failed",
                "payment_response": payment_response.json()
            }), 500

        REQUEST_COUNT.labels(endpoint="/orders", status=200).inc()
        REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)

        return jsonify({
            "service": "order-service",
            "order_id": 101,
            "status": "created",
            "payment": payment_response.json()
        })

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="/orders", status=500).inc()
        REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)
        return jsonify({"error": "Order Service failed to reach Payment Service", "details": str(e)}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)