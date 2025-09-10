import pytest
from loguru import logger

from src.common.functions import get_uuid
from src.model.product import Product

from . import client, headers
from src.database.database import Database

@pytest.fixture(autouse=True)
def setup_and_teardown(request):
    if "skip_setup" in request.keywords:
        yield
        return
    
    logger.info("Inserting initial customer for tests...")
    database = Database()
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
    database.products.insert(product)
    
    yield
    logger.info("Cleaning customer table after test...")
    database = Database()
    database.products.delete_all_products()

def test_get_all_products_with_cache():
    params = {
        "with_cache": True,
        "page": 1,
        "size": 10
    }
    response = None
    response_data = None

    with client:
        response = client.get("/v1/products/all", headers=headers, params=params)
        response_data = response.json()

    assert response.status_code == 200
    assert len(response_data["products"]) == 1



def test_get_all_products_without_cache():
    params = {
        "with_cache": False,
        "page": 1,
        "size": 10
    }

    with client:
        response = client.get("/v1/products/all", headers=headers, params=params)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data["products"]) == 10

@pytest.mark.skip_setup
def test_get_all_products_not_found():
    params = {
        "with_cache": True,
        "page": 1,
        "size": 10
    }
    response = None
    response_data = None

    with client:
        response = client.get("/v1/products/all", headers=headers, params=params)
        response_data = response.json()

    assert response.status_code == 200
    assert len(response_data["products"]) == 0

def test_get_product_by_api_id_with_cache():
    
    params = {
        "product_api_id": -1,
        "with_cache": True,
    }

    with client:
        response = client.get("/v1/products/by-api-id", headers=headers, params=params)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["product_api_id"] == -1

def test_get_product_by_api_id_with_cache_not_found():
    
    params = {
        "product_api_id": -2,
        "with_cache": True,
    }

    with client:
        response = client.get("/v1/products/by-api-id", headers=headers, params=params)
        response_data = response.json()

        assert response.status_code == 404
        assert response_data["error"] == "Product not found"

def test_get_product_by_api_id_without_cache():
    
    params = {
        "product_api_id": 1,
        "with_cache": False,
    }

    with client:
        response = client.get("/v1/products/by-api-id", headers=headers, params=params)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["product_api_id"] == 1

def test_get_product():
    database = Database()
    product = Product(
        product_api_id=-2,
        title="Initial Test",
        description="Initial Description",
        price=10.0,
        image="http://example.com/image.jpg",
        category = "electronics",
        rating_rate = 3.5,
        rating_count = 10

    )
    database.products.insert(product)
    product_id = product.product_id
    with client:

        response = client.get(f"/v1/products/id/{product_id}", headers=headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["product_api_id"] == -2

def test_get_product_not_found():
    product_id = get_uuid()
    with client:

        response = client.get(f"/v1/products/id/{product_id}", headers=headers)
        response_data = response.json()

        assert response.status_code == 404
        assert response_data["error"] == "Product not found"

def test_get_product_error():
    product_id = "invalid-uuid"
    with client:

        response = client.get(f"/v1/products/id/{product_id}", headers=headers)
        response_data = response.json()

        assert response.status_code == 500
        assert response_data["error"] == "Failed to retrieve product"