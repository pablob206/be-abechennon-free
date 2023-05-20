"""Api routes"""
# Third-Party
from fastapi import APIRouter

# App
import app.api.routes.root_route as root


api_router = APIRouter()
api_router.include_router(root.router, tags=["Info"])
