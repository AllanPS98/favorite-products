import pytest
from loguru import logger

from src.model.customer import Customer
from src.model.favorite import Favorite
from src.model.product import Product

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
    database.customers.insert(customer)
    database.products.insert(product)
    
    yield
    logger.info("Cleaning customer table after test...")
    database = Database()
    database.customers.delete_all_customers()
    database.products.delete_all_products()

#TODO: TESTAR CASOS DE ERRO
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
