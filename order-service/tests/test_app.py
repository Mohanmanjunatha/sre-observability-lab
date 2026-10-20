
import importlib.util
from pathlib import Path
from unittest.mock import patch, Mock

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"

spec = importlib.util.spec_from_file_location("order_app", APP_PATH)
order_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(order_app)

app = order_app.app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["service"] == "order-service"


def test_order_success():
    client = app.test_client()

    mock_payment = Mock()
    mock_payment.status_code = 200
    mock_payment.json.return_value = {
        "payment_status": "success"
    }

    with patch.object(order_app.requests, "get", return_value=mock_payment), \
         patch.object(order_app.time, "sleep"):
        response = client.get("/orders")

    assert response.status_code == 200
    assert response.json["status"] == "created"
    assert response.json["order_id"] == 101


def test_order_payment_failure():
    client = app.test_client()

    mock_payment = Mock()
    mock_payment.status_code = 500
    mock_payment.json.return_value = {
        "payment_status": "failed"
    }

    with patch.object(order_app.requests, "get", return_value=mock_payment), \
         patch.object(order_app.time, "sleep"):
        response = client.get("/orders")

    assert response.status_code == 500
    assert "error" in response.json
