from fastapi import FastAPI
from src.routes.health_check import router as health_check_router
from src.configurations import Configurations

configurations = Configurations()

def create_app():
    application = FastAPI(
        title=configurations.APP_NAME,
        version=configurations.APP_VERSION,
    )
    application.include_router(health_check_router, tags=["Health Check"])
    return application

app = create_app()