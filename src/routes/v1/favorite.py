from fastapi import APIRouter
from src.controller.favorite import FavoriteController
from src.schema.customer import GetCustomerErrorResponse
from src.schema.favorite import PostFavoritePayload, RemoveFavoriteErrorResponse, RemoveFavoriteSuccessResponse, SetFavoriteErrorResponse, SetFavoriteSuccessResponse
from src.schema.favorite import GetFavoriteParams
from src.schema.favorite import ListFavoriteResponse
from src.schema.favorite import DeleteFavoriteParams

router = APIRouter(prefix="/favorites")

@router.post(
    "", 
    status_code=201, 
    summary="Set a product as favorite for a customer", 
    responses={
        201: {
            "description": "Favorite set successfully",
            "model": SetFavoriteSuccessResponse
        },
        500: {
            "description": "Failed to set favorite",
            "model": SetFavoriteErrorResponse
        }
    }
)
def set_favorite(payload: PostFavoritePayload):
    controller = FavoriteController()
    response_data = controller.set_favorite(payload)
    return response_data

@router.get(
    "/customer", 
    status_code=200, 
    summary="Get all favorite products for a customer", 
    responses={
        200: {
            "description": "List of favorite products",
            "model": ListFavoriteResponse
        },
        500: {
            "description": "Failed to retrieve favorites",
            "model": GetCustomerErrorResponse
        }
    }
)
def get_favorites_by_customer(customer_id: str, page: int = 1, size: int = 10):
    params = GetFavoriteParams(
        customer_id=customer_id,
        page=page,
        size=size
    )
    controller = FavoriteController()
    response_data = controller.get_favorites_by_customer(params)
    return response_data

@router.delete(
    "", 
    status_code=200, 
    summary="Remove a product from customer's favorites", 
    responses={
        200: {
            "description": "Favorite removed successfully",
            "model": RemoveFavoriteSuccessResponse
        },
        500: {
            "description": "Failed to remove favorite",
            "model": RemoveFavoriteErrorResponse
        }
    }
)
def remove_favorite(customer_id: str, product_id: str):
    params = DeleteFavoriteParams(
        customer_id=customer_id,
        product_id=product_id
    )
    controller = FavoriteController()
    response_data = controller.remove_favorite(params)
    return response_data

