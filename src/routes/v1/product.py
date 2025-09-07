from typing import List
from fastapi import APIRouter
from src.schema.product import GetAllProductsParams, GetProductByApiIdParams, GetProductResponse
from src.controller.product import ProductController

router = APIRouter(prefix="/products")

#TODO: improve swagger documentation
@router.get(
    "", 
    status_code=200, 
    summary="Get all products", 
    responses={200: {"description": "List of products", "model": List[GetProductResponse]}}
)
def get_products(params: GetAllProductsParams):
    controller = ProductController()
    response_data = controller.get_all_products(params)
    return response_data

@router.get(
    "/by-api-id", 
    status_code=200, 
    summary="Get product by API ID", 
    responses={200: {"description": "Product details", "model": GetProductResponse}}
)
def get_product_by_api_id(params: GetProductByApiIdParams):
    controller = ProductController()
    response_data = controller.get_product_by_api_id(params)
    return response_data

@router.get(
    "/id/{product_id}", 
    status_code=200, 
    summary="Get product by internal ID", 
    responses={200: {"description": "Product details", "model": GetProductResponse}}
)
def get_product(product_id: str):
    controller = ProductController()
    response_data = controller.get_product(product_id)
    return response_data