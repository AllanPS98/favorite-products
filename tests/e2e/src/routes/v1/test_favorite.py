from . import client, headers

def test_set_favorite():
    customer_email = "test@gmail.com"
    product_api_id = 1
    with client:
        response_customer = client.post(
            "/v1/customers",
            headers=headers,
            json={
                "name": "Test Name",
                "email": customer_email
            }
        )
        customer_id = response_customer.json()["customer_id"]
        response_customer.raise_for_status()
        response_product = client.get(
            "/v1/products/by-api-id",
            headers=headers,
            params={
                "product_api_id": product_api_id,
                "with_cache": False
            }
        )
        product_id = response_product.json()["product_id"]
        response_product.raise_for_status()
        response = client.post(
            "/v1/favorites",
            headers=headers,
            json={
                "customer_email": customer_email,
                "product_api_id": product_api_id
            }
        )
        response_data = response.json()
        client.delete("v1/favorites", headers=headers, params={
            "customer_id": customer_id,
            "product_id": product_id
        })
        client.delete(f"/v1/customers/{customer_id}", headers=headers)
        assert response.status_code == 201
        assert response_data["message"] == "Favorite set successfully"