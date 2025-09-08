from typing import List
from fastapi import APIRouter
from src.schema.product import GetAllProductsErrorResponse, GetAllProductsParams, GetProductByApiIdErrorResponse, GetProductByApiIdNotFoundResponse, GetProductByApiIdParams, GetProductErrorResponse, GetProductNotFoundResponse, GetProductResponse, ListProductResponse
from src.controller.product import ProductController

router = APIRouter(prefix="/products")

@router.get(
    "/all", 
    status_code=200, 
    summary="Get all products", 
    responses={
        200: {
            "description": "List of products", 
            "model": ListProductResponse
        },
        500: {
            "description": "Failed to retrieve products",
            "model": GetAllProductsErrorResponse
        }
    }
)
def get_products(params: GetAllProductsParams):
    controller = ProductController()
    response_data = controller.get_all_products(params)
    return response_data

@router.get(
    "/by-api-id", 
    status_code=200, 
    summary="Get product by API ID", 
    responses={
        200: {
            "description": "Product details",
            "model": GetProductResponse
        },
        404: {
            "description": "Product not found",
            "model": GetProductByApiIdNotFoundResponse
        },
        500: {
            "description": "Failed to retrieve product",
            "model": GetProductByApiIdErrorResponse
        }
    }
)
def get_product_by_api_id(params: GetProductByApiIdParams):
    controller = ProductController()
    response_data = controller.get_product_by_api_id(params)
    return response_data

@router.get(
    "/id/{product_id}", 
    status_code=200, 
    summary="Get product by internal ID", 
    responses={
        200: {
            "description": "Product details",
            "model": GetProductResponse
        },
        404: {
            "description": "Product not found",
            "model": GetProductNotFoundResponse
        },
        500: {
            "description": "Failed to retrieve product",
            "model": GetProductErrorResponse
        }
    }
)
def get_product(product_id: str):
    controller = ProductController()
    response_data = controller.get_product(product_id)
    return response_data