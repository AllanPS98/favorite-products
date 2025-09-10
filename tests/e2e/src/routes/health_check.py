from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)
headers = {"Content-Type": "application/json"}

def test_health_check():
    with client:
        response = client.get("/health-check", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}