from typing import List
from pydantic import BaseModel
from src.schema.product import GetProductResponse


class PostFavoritePayload(BaseModel):
    customer_id: str
    product_id: str

class ListFavoriteResponse(BaseModel):
    page: int
    size: int
    total: int
    customer_id: str
    products: List[GetProductResponse]

class GetFavoriteResponse(BaseModel):
    customer_id: str
    product: GetProductResponse

class GetFavoriteParams(BaseModel):
    page: int
    size: int
    customer_id: str
    
class DeleteFavoriteParams(BaseModel):
    customer_id: str
    product_id: str
