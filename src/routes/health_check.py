from typing import Dict
from fastapi import APIRouter

router = APIRouter()

@router.get("/health-check", tags=["Health Check"], summary="Health Check Endpoint", status_code=200, responses={
    200: {"description": "Service is healthy", "content": {"application/json": {"example": {"status": "ok"}}}}
})
async def get_health_check() -> Dict:
    return {"status": "ok"}