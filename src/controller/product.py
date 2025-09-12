from http import HTTPStatus
from fastapi import Response
from loguru import logger

from src.common.functions import get_uuid
from src.integration.fake_store import FakeStore
from src.database.database import Database
from src.model.product import Product
from src.schema.product import GetAllProductsErrorResponse, GetAllProductsParams, GetProductByApiIdErrorResponse
from src.schema.product import GetProductByApiIdNotFoundResponse, GetProductByApiIdParams, GetProductErrorResponse
from src.schema.product import GetProductNotFoundResponse, GetProductResponse, ListProductResponse
from src.constants import APPLICATION_JSON


class ProductController:

    def __init__(self):
        pass
    
    @property
    def __fake_store(self) -> FakeStore:
        return FakeStore()

    @property
    def __database(self) -> Database:
        return Database()
    
    def __insert_product(self, product_api_id: int, with_cache: bool):
        if not with_cache:
            product_response = self.__fake_store.get_product_by_api_id(product_api_id)
            if product_response:
                product_object = Product(
                    product_id=get_uuid(),
                    product_api_id=product_response.get("id"),
                    title=product_response.get("title"),
                    price=product_response.get("price"),
                    description=product_response.get("description"),
                    category=product_response.get("category"),
                    image=product_response.get("image"),
                    rating_rate=product_response.get("rating", {}).get("rate"),
                    rating_count=product_response.get("rating", {}).get("count")
                )
                old_product = self.__database.products.get_product_by_api_id(product_api_id)
                if not old_product:
                    logger.info(f"Inserting product with API ID {product_api_id}")
                    self.__database.products.insert(product_object)
                    return
                logger.info(f"Updating product with API ID {product_api_id}")
                product_id = old_product.product_id
                product_dict = product_object.get().copy()
                product_dict.pop("product_id")
                self.__database.products.update(product_id, product_dict)
    
    def __insert_all_products(self, with_cache: bool):
        to_insert_results = list[dict]()
        to_update_results = list[dict]()
        if not with_cache:
            products_response = self.__fake_store.get_products()
            for product_data in products_response:
                product_model_dict = {
                    "product_api_id": product_data.get("id"),
                    "title": product_data.get("title"),
                    "price": product_data.get("price"),
                    "description": product_data.get("description"),
                    "category": product_data.get("category"),
                    "image": product_data.get("image"),
                    "rating_rate": product_data.get("rating", {}).get("rate"),
                    "rating_count": product_data.get("rating", {}).get("count")
                }
                existing_product = self.__database.products.get_product_by_api_id(product_model_dict.get("product_api_id"))
                if existing_product:
                    product_model_dict["product_id"] = existing_product.product_id
                    to_update_results.append(product_model_dict)
                    continue
                product_model_dict["product_id"] = get_uuid()
                to_insert_results.append(product_model_dict)
        self.__database.products.insert_all(to_insert_results)
        self.__database.products.update_all(to_update_results) 

    def get_all_products(self, params: GetAllProductsParams) -> Response:
        with_cache = params.with_cache
        page = params.page
        size = params.size
        try:
            self.__insert_all_products(with_cache)
            products, total = self.__database.products.get_all_products(page, size)
            results = [GetProductResponse(**product.get()) for product in products]
            product_list = ListProductResponse(
                page=page,
                size=size,
                total=total,
                products=results
            )
            response = Response(content=product_list.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
            logger.info("Products retrieved successfully")
        except Exception as e:
            error = GetAllProductsErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to retrieve products: {e}")
        finally:
            return response          

    def get_product(self, product_id: str) -> Response:
        try:
            error = GetProductNotFoundResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
            product = self.__database.products.get_product(product_id)
            if product:
                result = GetProductResponse(**product.get())
                response = Response(content=result.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
                logger.info("Product retrieved successfully")
        except Exception as e:
            error = GetProductErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to retrieve product: {e}")
        finally:
            return response

    def get_product_by_api_id(self, params: GetProductByApiIdParams) -> Response:
        product_api_id = params.product_api_id
        with_cache = params.with_cache
        try:
            error = GetProductByApiIdNotFoundResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
            self.__insert_product(product_api_id, with_cache)
            product = self.__database.products.get_product_by_api_id(product_api_id)
            if product:
                result = GetProductResponse(**product.get())
                response = Response(content=result.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
                logger.info("Product retrieved successfully")
        except Exception as e:
            error = GetProductByApiIdErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to retrieve product: {e}")
        finally:
            return response
