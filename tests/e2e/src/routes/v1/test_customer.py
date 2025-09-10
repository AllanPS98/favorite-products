from . import client, headers

def test_create_customer():
    customer_name = "Test Name"
    customer_email = "test@gmail.com"
    payload = {
        "name": customer_name,
        "email": customer_email
    }
    with client:
        response = client.post("/v1/customers", headers=headers, json=payload)
        response_data = response.json()
        customer_id = response_data["customer_id"]
        client.delete(f"/v1/customers/{customer_id}", headers=headers)
        assert response.status_code == 201
        assert response_data["message"] == "Customer created successfully"