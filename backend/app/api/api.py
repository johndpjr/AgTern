from fastapi import APIRouter

from .endpoints import jobs, login

api_router = APIRouter()
api_router.include_router(jobs, prefix="/jobs", tags=["jobs"])
api_router.include_router(login, prefix="/login", tags=["login"])
