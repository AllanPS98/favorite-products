import pytest
from loguru import logger

from src.common.functions import get_uuid
from src.model.customer import Customer
from src.model.favorite import Favorite
from src.model.product import Product

from . import client, do_login, headers
from src.database.database import Database
from src.configurations import Configurations

configurations = Configurations()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    logger.info("Inserting initial customer for tests...")
    database = Database()
    customer = Customer(
        name="Initial Test",
        email="initialtest@gmail.com",
        encrypted_password="test1234"
    )
    product = Product(
        product_api_id=-1,
        title="Initial Test",
        description="Initial Description",
        price=10.0,
        image="http://example.com/image.jpg",
        category = "electronics",
        rating_rate = 3.5,
        rating_count = 10

    )
    database.customers.delete_all_customers()
    database.products.delete_all_products()
    database.customers.insert(customer)
    database.products.insert(product)
    do_login()
    
    yield
    logger.info("Cleaning customer table after test...")
    database = Database()
    database.customers.delete_all_customers()
    database.products.delete_all_products()

def test_set_favorite():
    customer_email = "initialtest@gmail.com"
    product_api_id = -1
    with client:
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 201
        assert response_data["message"] == "Favorite set successfully"

def test_set_favorite_duplicated():
    customer_email = "initialtest@gmail.com"
    product_api_id = -1
    with client:
        client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["error"] == "This favorite product is already exists for this customer"

def test_set_favorite_not_found_customer():
    customer_email = "initial@gmail.com"
    product_api_id = -1
    with client:
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["error"] == "Customer not found"

def test_set_favorite_not_found_product():
    customer_email = "initialtest@gmail.com"
    product_api_id = -2
    with client:
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["error"] == "Product not found"

def test_set_favorite_wrong_customer_email():
    customer_email = "initialtest@gmai.com"
    product_api_id = -1
    with client:
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["error"] == "Customer not found"

def test_set_favorite_wrong_product_api_id():
    customer_email = "initialtest@gmail.com"
    product_api_id = "a"
    with client:
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        assert response.status_code == 422

def test_get_favorites_by_customer():
    database = Database()
    customer_email = "initialtest@gmail.com"
    product_api_id = -1
    customer = database.customers.get_by_email(customer_email)
    customer_id = str(customer.customer_id)
    product = database.products.get_product_by_api_id(product_api_id)
    product_id = str(product.product_id)
    favorite = Favorite(
        customer_id=customer_id,
        product_id=product_id
    )
    database.favorites.set_favorite(favorite)
    with client:
        response = client.get(
            "/v1/favorites/customer",
            headers=headers,
            params={
                "customer_id": customer_id,
                "page": 1,
                "size": 10
            }
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["customer_id"] == customer_id
        assert len(response_data["products"]) == 1
        assert response_data["products"][0]["product_api_id"] == -1

def test_get_favorites_by_customer_not_found():
    customer_id = get_uuid()
    with client:
        response = client.get(
            "/v1/favorites/customer",
            headers=headers,
            params={
                "customer_id": customer_id,
                "page": 1,
                "size": 10
            }
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["products"] == []

def test_get_favorites_by_customer_error():
    customer_id = "invalid-uuid"
    with client:
        response = client.get(
            "/v1/favorites/customer",
            headers=headers,
            params={
                "customer_id": customer_id,
                "page": 1,
                "size": 10
            }
        )
        response_data = response.json()
        assert response.status_code == 500
        assert response_data["error"] == "Failed to retrieve favorites"

def test_remove_favorite():
    database = Database()
    customer_email = "initialtest@gmail.com"
    product_api_id = -1
    customer = database.customers.get_by_email(customer_email)
    customer_id = str(customer.customer_id)
    product = database.products.get_product_by_api_id(product_api_id)
    product_id = str(product.product_id)
    favorite = Favorite(
        customer_id=customer_id,
        product_id=product_id
    )
    database.favorites.set_favorite(favorite)
    with client:
        response = client.delete(
            "/v1/favorites",
            headers=headers,
            params={
                "customer_id": customer_id,
                "product_id": product_id
            }
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "Favorite removed successfully"

def test_remove_favorite_not_found():
    customer_id = get_uuid()
    product_id = get_uuid()
    with client:
        response = client.delete(
            "/v1/favorites",
            headers=headers,
            params={
                "customer_id": customer_id,
                "product_id": product_id
            }
        )
        response_data = response.json()
        assert response.status_code == 404
        assert response_data["error"] == "Favorite not found"

def test_remove_favorite_error():
    customer_id = "invalid-uuid"
    product_id = get_uuid()
    with client:
        response = client.delete(
            "/v1/favorites",
            headers=headers,
            params={
                "customer_id": customer_id,
                "product_id": product_id
            }
        )
        response_data = response.json()
        assert response.status_code == 500
        assert response_data["error"] == "Failed to remove favorite"
