from fastapi import FastAPI
from src.routes.health_check import router as health_check_router
from src.routes.v1 import v1
from src.configurations import Configurations
from src.tracing import TracingMiddleware

configurations = Configurations()

def create_app():
    application = FastAPI(
        title=configurations.APP_NAME,
        version=configurations.APP_VERSION,
    )
    application.add_middleware(TracingMiddleware)
    application.include_router(health_check_router)
    application.include_router(v1)
    return application

app = create_app()