from fastapi import APIRouter

from api.api_v1.endpoints import patient

api_router = APIRouter()
api_router.include_router(patient.router, prefix="/patients", tags=["patients"])

