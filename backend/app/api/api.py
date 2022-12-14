from fastapi import APIRouter

from .endpoints import internships

api_router = APIRouter()
api_router.include_router(internships, prefix="/internships", tags=["internships"])
