from typing import List
from fastapi import APIRouter
from src.controller.favorite import FavoriteController
from src.schema.favorite import PostFavoritePayload
from src.schema.favorite import GetFavoriteParams
from src.schema.favorite import ListFavoriteResponse
from src.schema.favorite import DeleteFavoriteParams

router = APIRouter(prefix="/favorites")

#TODO: improve swagger documentation
@router.post(
    "", 
    status_code=201, 
    summary="Set a product as favorite for a customer", 
    responses={201: {"description": "Favorite set successfully"}}
)
def set_favorite(payload: PostFavoritePayload):
    controller = FavoriteController()
    response_data = controller.set_favorite(payload)
    return response_data

@router.get(
    "/customer", 
    status_code=200, 
    summary="Get all favorite products for a customer", 
    responses={200: {"description": "List of favorite products", "model": ListFavoriteResponse}}
)
def get_favorites_by_customer(params: GetFavoriteParams):
    controller = FavoriteController()
    response_data = controller.get_favorites_by_customer(params)
    return response_data

@router.delete(
    "", 
    status_code=200, 
    summary="Remove a product from customer's favorites", 
    responses={200: {"description": "Favorite removed successfully"}}
)
def remove_favorite(params: DeleteFavoriteParams):
    controller = FavoriteController()
    response_data = controller.remove_favorite(params)
    return response_data

