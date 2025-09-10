from . import client, headers

def test_get_all_products_with_cache():
    #TODO: INSERIR ANTES DE BUSCAR E REMOVER DEPOIS DE BUSCAR (USAR UM PRODUTO MOCKADO DE TESTE)
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
    assert len(response_data["products"]) == 10

def test_get_all_products_without_cache():
    # TODO: INSERIR ANTES DE BUSCAR E REMOVER DEPOIS DE BUSCAR (USAR UM PRODUTO MOCKADO DE TESTE)
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

def test_get_product_by_api_id_with_cache():
    # TODO: INSERIR ANTES DE BUSCAR E REMOVER DEPOIS DE BUSCAR (USAR UM PRODUTO MOCKADO DE TESTE)
    params = {
        "product_api_id": 1,
        "with_cache": True,
    }

    with client:
        response = client.get("/v1/products/by-api-id", headers=headers, params=params)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["product_api_id"] == 1

def test_get_product_by_api_id_without_cache():
    # TODO: INSERIR ANTES DE BUSCAR E REMOVER DEPOIS DE BUSCAR (USAR UM PRODUTO MOCKADO DE TESTE)
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
    # TODO: INSERIR ANTES DE BUSCAR E REMOVER DEPOIS DE BUSCAR (USAR UM PRODUTO MOCKADO DE TESTE)
    params = {
        "with_cache": False,
        "page": 1,
        "size": 10
    }
    
    with client:
        response_all = client.get("/v1/products/all", headers=headers, params=params)    
        response_all_data = response_all.json()
        product_id = response_all_data["products"][0]["product_id"]

        response = client.get(f"/v1/products/id/{product_id}", headers=headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["product_api_id"] == 1