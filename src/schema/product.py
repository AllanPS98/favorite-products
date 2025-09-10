from typing import List, Optional
from pydantic import BaseModel

class GetProductResponse(BaseModel):
    product_id: str
    product_api_id: int
    title: str
    price: float
    description: Optional[str]
    category: str
    image: str
    rating_rate: Optional[float]
    rating_count: Optional[int]

class ListProductResponse(BaseModel):
    page: int
    size: int
    total: int
    products: List[GetProductResponse]

class GetAllProductsParams(BaseModel):
    with_cache: bool
    page: int
    size: int

class GetProductByApiIdParams(BaseModel):
    product_api_id: int
    with_cache: bool
    
class GetProductByApiIdErrorResponse(BaseModel):
    error: str = "Failed to retrieve product"

class GetProductByApiIdNotFoundResponse(BaseModel):
    error: str = "Product not found"

class GetAllProductsErrorResponse(BaseModel):
    error: str = "Failed to retrieve products"

class GetProductErrorResponse(BaseModel):
    error: str = "Failed to retrieve product"

class GetProductNotFoundResponse(BaseModel):
    error: str = "Product not found"
