from requests import Session
from . import client

headers = {"Content-Type": "application/json"}

def test_get_all_products():
    params = {
        "with_cache": True,
        "page": 1,
        "size": 10
    }
    response = None
    response_data = None

    with client:
        response = client.get(f"/v1/products/all", headers=headers, params=params)
        response_data = response.json()

    assert response.status_code == 200
    assert len(response_data["products"]) == 10