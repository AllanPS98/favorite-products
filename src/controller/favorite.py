from typing import List
from fastapi import Response
from loguru import logger
from http import HTTPStatus

from src.database.database import Database
from src.model.favorite import Favorite
from src.schema.exceptions import SetFavoriteCustomerNotFoundError, SetFavoriteProductNotFoundError
from src.schema.favorite import GetFavoriteErrorResponse, ListFavoriteResponse, PostFavoritePayload, RemoveFavoriteErrorResponse, RemoveFavoriteSuccessResponse, SetFavoriteErrorCustomerNotFoundResponse, SetFavoriteErrorProductNotFoundResponse, SetFavoriteErrorResponse, SetFavoriteSuccessResponse 
from src.schema.favorite import GetFavoriteParams
from src.schema.favorite import DeleteFavoriteParams
from src.constants import APPLICATION_JSON
from src.schema.product import GetProductResponse

class FavoriteController:
    
    def __init__(self):
        pass

    @property
    def __database(self) -> Database:
        return Database()
    
    def __append_resuts(self, customer_id: str, favorites: List, results: List[GetProductResponse]):
        for product_id in favorites:
            product = self.__database.products.get_product(str(product_id[0]))
            if product:
                result = GetProductResponse(**product.get())
                results.append(result)

    def set_favorite(self, payload: PostFavoritePayload) -> Response:
        try:
            customer = self.__database.customers.get_by_email(payload.customer_email)
            if not customer:
                error = SetFavoriteErrorCustomerNotFoundResponse()
                response = Response(content=error.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
                raise SetFavoriteCustomerNotFoundError(error.error)
            product = self.__database.products.get_product_by_api_id(payload.product_api_id)
            if not product:
                error = SetFavoriteErrorProductNotFoundResponse()
                response = Response(content=error.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
                raise SetFavoriteProductNotFoundError(error.error)
            customer_id = customer.get()["customer_id"]
            product_id = product.get()["product_id"]
            favorite_object = Favorite(customer_id=customer_id, product_id=product_id)
            self.__database.favorites.set_favorite(favorite_object)
            success = SetFavoriteSuccessResponse()
            response = Response(content=success.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.CREATED)
            logger.info(success.message)
        except SetFavoriteCustomerNotFoundError | SetFavoriteProductNotFoundError as not_found_exception:
            logger.exception(f"Failed to set favorite: {not_found_exception}")
        except Exception as e:
            error = SetFavoriteErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to set favorite: {e}")
        finally:
            return response

    def get_favorites_by_customer(self, params: GetFavoriteParams) -> Response:
        customer_id = params.customer_id
        page = params.page
        size = params.size
        try:
            favorites, total = self.__database.favorites.get_favorites_by_customer(customer_id, page, size)
            results = list[GetProductResponse]()
            self.__append_resuts(customer_id, favorites, results)
            favorite_list = ListFavoriteResponse(
                page=page,
                size=size,
                total=total,
                customer_id=customer_id,
                products=results
            )
            response = Response(content=favorite_list.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
            logger.info("Favorites retrieved successfully")
        except Exception as e:
            error = GetFavoriteErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to retrieve favorites: {e}")
        finally:
            return response

    def remove_favorite(self, params: DeleteFavoriteParams) -> Response:
        customer_id = params.customer_id
        product_id = params.product_id
        try:
            self.__database.favorites.remove_favorite(customer_id, product_id)
            success = RemoveFavoriteSuccessResponse()
            response = Response(content=success.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
            logger.info(success.message)
        except Exception as e:
            error = RemoveFavoriteErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to remove favorite: {e}")
        finally:
            return response