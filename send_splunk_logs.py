
import json
import os
import random
import ssl
import urllib.request
from datetime import datetime, timezone

token = os.environ.get("SPLUNK_HEC_TOKEN")

if not token:
    raise SystemExit("SPLUNK_HEC_TOKEN is not set")

url = "https://localhost:8088/services/collector/event"
context = ssl._create_unverified_context()  # Local lab only

services = ["api-gateway", "order-service", "payment-service"]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/orders", "/pay", "/health", "/api/orders"]

# Documentation-only IP ranges for safe lab testing
source_ips = [
    "192.0.2.10",
    "192.0.2.25",
    "198.51.100.15",
    "198.51.100.45"
]

destination_ips = [
    "203.0.113.10",
    "203.0.113.20",
    "203.0.113.30"
]

for i in range(200):
    service = random.choice(services)
    status = random.choices(
        [200, 201, 400, 404, 500, 502, 503],
        weights=[50, 10, 10, 10, 10, 5, 5]
    )[0]

    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": service,
        "src_ip": random.choice(source_ips),
        "dest_ip": random.choice(destination_ips),
        "src_port": random.randint(1024, 65535),
        "dest_port": 5000,
        "protocol": "HTTP",
        "method": random.choice(methods),
        "path": random.choice(paths),
        "status": status,
        "latency_ms": random.randint(10, 2000),
        "request_id": f"req-{i+1}",
        "message": "Request completed" if status < 400 else "Request failed"
    }

    payload = {
        "index": "main",
        "sourcetype": "_json",
        "source": "sre-lab-network-simulation",
        "event": log
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Splunk {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, context=context) as response:
        result = json.loads(response.read())
        if result.get("code") != 0:
            raise RuntimeError(f"Splunk HEC error: {result}")

    print(
        f"{log['src_ip']}:{log['src_port']} -> "
        f"{log['dest_ip']}:{log['dest_port']} "
        f"{service} HTTP {status}"
    )

print("Successfully sent 200 synthetic network-style logs!")
