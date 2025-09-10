import pytest
from loguru import logger

from src.model.customer import Customer

from . import client, headers
from src.database.database import Database

@pytest.fixture(autouse=True)
def setup_and_teardown():
    logger.info("Inserting initial customer for tests...")
    database = Database()
    customer = Customer(
        name="Initial Test",
        email="initialtest@gmail.com"
    )
    database.customers.insert(customer)
    
    yield
    logger.info("Cleaning customer table after test...")
    database = Database()
    database.customers.delete_all_customers()

#TODO: TESTAR CASOS DE ERRO
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
        assert response.status_code == 201
        assert response_data["message"] == "Customer created successfully"
        assert response_data["customer_id"] is not None

def test_get_customer():
    customer_name = "Test Name"
    customer_email = "test@gmail.com"
    payload = {
        "name": customer_name,
        "email": customer_email
    }
    with client:
        response_create = client.post("/v1/customers", headers=headers, json=payload)
        response_create_data = response_create.json()
        customer_id = response_create_data["customer_id"]
        response = client.get(f"/v1/customers/id/{customer_id}", headers=headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["customer_id"] == customer_id
        assert response_data["name"] == customer_name
        assert str(response_data["email"]).startswith(customer_email[0])

def test_get_customer_by_email():
    with client:
        response = client.get(f"/v1/customers/by-email", headers=headers, params={"customer_email": "initialtest@gmail.com"})
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["customer_id"] is not None
        assert response_data["name"] == "Initial Test"
        assert str(response_data["email"]).startswith("i")

def test_update_customer():
    customer_name = "Test Name"
    customer_email = "test@gmail.com"
    payload = {
        "name": customer_name,
        "email": customer_email
    }
    with client:
        response_create = client.post("/v1/customers", headers=headers, json=payload)
        response_create_data = response_create.json()
        customer_id = response_create_data["customer_id"]
        response = client.put(f"/v1/customers/{customer_id}", headers=headers, json={"name": "Updated Name"})
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "Customer updated successfully"

def test_delete_customer():
    customer_name = "Test Name"
    customer_email = "test@gmail.com"
    payload = {
        "name": customer_name,
        "email": customer_email
    }
    with client:
        response_create = client.post("/v1/customers", headers=headers, json=payload)
        response_create_data = response_create.json()
        customer_id = response_create_data["customer_id"]
        response = client.delete(f"/v1/customers/{customer_id}", headers=headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "Customer deleted successfully"