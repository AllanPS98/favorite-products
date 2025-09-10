from typing import List
from pydantic import BaseModel
from src.schema.product import GetProductResponse


class PostFavoritePayload(BaseModel):
    customer_email: str
    product_api_id: int

class ListFavoriteResponse(BaseModel):
    page: int
    size: int
    total: int
    customer_id: str
    products: List[GetProductResponse]

class GetFavoriteParams(BaseModel):
    page: int
    size: int
    customer_id: str
    
class DeleteFavoriteParams(BaseModel):
    customer_id: str
    product_id: str

class SetFavoriteSuccessResponse(BaseModel):
    message: str = "Favorite set successfully"

class SetFavoriteErrorCustomerNotFoundResponse(BaseModel):
    error: str = "Customer not found"

class SetFavoriteErrorProductNotFoundResponse(BaseModel):
    error: str = "Product not found"

class SetFavoriteErrorResponse(BaseModel):
    error: str = "Failed to set favorite"

class GetFavoriteErrorResponse(BaseModel):
    error: str = "Failed to retrieve favorites"

class RemoveFavoriteSuccessResponse(BaseModel):
    message: str = "Favorite removed successfully"

class RemoveFavoriteErrorResponse(BaseModel):
    error: str = "Failed to remove favorite"
