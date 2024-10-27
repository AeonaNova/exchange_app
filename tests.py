from fastapi.testclient import TestClient
import main
import pytest
app = main.app
client = TestClient(app)

def test_interaction():
    uuid = '1s'
    response = client.post(f"/api/v1/wallets/{uuid}/operation", params={"balance": 45.0, "operation": "DEPOSIT"})
    assert response.status_code == 200
    response_wdraw = client.post(f"/api/v1/wallets/{uuid}/operation", params={"balance": 3.84, "operation": "WITHDRAW"})
    assert response_wdraw.status_code == 200
    response_get = client.get(f"/api/v1/wallets/{uuid}")
    assert response_get.status_code == 200

def test_get_new_wallet():
    uuid = "2f"
    response = client.get(f"/api/v1/wallets/{uuid}")
    assert response.status_code == 200
    data = response.json()
    assert "balance:" in data
    assert data["balance:"] == 0.0