"""Api routes"""
# Third-Party
from fastapi import APIRouter

# App
import app.api.api_v1.routes.root_route as root
import app.api.api_v1.routes.settings_route as settings
import app.api.api_v1.routes.bot_route as bot


api_router = APIRouter()
api_router.include_router(root.router, tags=["Info"])
api_router.include_router(settings.router, tags=["Settings"])
api_router.include_router(bot.router, tags=["Bot"])
