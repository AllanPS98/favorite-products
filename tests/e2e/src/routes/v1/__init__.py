from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)
headers = {"Content-Type": "application/json"}

def do_login():
    customer_name = "Logged User"
    customer_email = "logged@gmail.com"
    customer_password = "test1234"
    payload = {
        "name": customer_name,
        "email": customer_email,
        "password": customer_password
    }
    client.post("/v1/customers", headers=headers, json=payload)
    response_login = client.post("/v1/customers/login", headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }, data=f"username={customer_email}&password={customer_password}")
    response_login_data = response_login.json()
    token = response_login_data["access_token"]
    headers["Authorization"] = f"Bearer {token}"