from typing import List, Optional
from pydantic import BaseModel

class GetProductResponse(BaseModel):
    product_id: str
    product_api_id: str
    title: str
    price: float
    description: Optional[str]
    category: str
    image: str
    rating_rate: Optional[float]
    rate_count: Optional[int]

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
    message: str = "Failed to retrieve product"

class GetProductByApiIdNotFoundResponse(BaseModel):
    message: str = "Product not found"

class GetAllProductsErrorResponse(BaseModel):
    message: str = "Failed to retrieve products"

class GetProductErrorResponse(BaseModel):
    message: str = "Failed to retrieve product"

class GetProductNotFoundResponse(BaseModel):
    message: str = "Product not found"
