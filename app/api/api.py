"""Api routes"""
# Third-Party
from fastapi import APIRouter

# App
import app.api.routes.root_route as root
import app.api.routes.settings_route as settings


api_router = APIRouter()
api_router.include_router(root.router, tags=["Info"])
api_router.include_router(settings.router, tags=["Settings"])
