from fastapi import APIRouter
from src.routes.v1.customer import router as customer_router
from src.routes.v1.favorite import router as favorite_router
from src.routes.v1.product import router as product_router

v1 = APIRouter(prefix="/v1")

v1.include_router(customer_router, tags=["Customers"])
v1.include_router(favorite_router, tags=["Favorites"])
v1.include_router(product_router, tags=["Products"])