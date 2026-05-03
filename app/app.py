from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)

@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return "SRE Observability Lab is running!"

@app.route("/api")
def api():
    start = time.time()
    REQUEST_COUNT.labels(endpoint="/api").inc()

    time.sleep(random.uniform(0.1, 0.7))

    REQUEST_LATENCY.labels(endpoint="/api").observe(time.time() - start)
    return {"message": "API response successful"}

@app.route("/error")
def error():
    REQUEST_COUNT.labels(endpoint="/error").inc()
    return {"error": "Something went wrong"}, 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
