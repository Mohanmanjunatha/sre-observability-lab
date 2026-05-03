from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time
import random
import requests

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "api_gateway_requests_total",
    "Total requests received by API Gateway",
    ["endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "api_gateway_request_latency_seconds",
    "API Gateway request latency",
    ["endpoint"]
)

@app.route("/")
def home():
    return "API Gateway is running"

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "api-gateway"})

@app.route("/orders")
def orders():
    start = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.4))

        response = requests.get("http://order-service:5000/orders", timeout=2)

        REQUEST_COUNT.labels(endpoint="/orders", status=response.status_code).inc()
        REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)

        return jsonify({
            "gateway": "api-gateway",
            "response_from_order_service": response.json()
        }), response.status_code

    except Exception as e:
        REQUEST_COUNT.labels(endpoint="/orders", status=500).inc()
        REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)

        return jsonify({
            "error": "API Gateway failed to reach Order Service",
            "details": str(e)
        }), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)