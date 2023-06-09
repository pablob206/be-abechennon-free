"""Api routes"""
# Third-Party
from fastapi import APIRouter

# App
import app.api.api_v1.routes.root_route as root
import app.api.api_v1.routes.setting_route as setting
import app.api.api_v1.routes.bot_route as bot
import app.api.api_v1.routes.strategy_route as strategy
import app.api.api_v1.routes.order_management_route as order_management
import app.api.api_v1.routes.loan_route as loan


api_router = APIRouter()
api_router.include_router(root.router, tags=["Info"])
api_router.include_router(setting.router, tags=["Setting"])
api_router.include_router(bot.router, tags=["Bot"])
api_router.include_router(order_management.router, tags=["Order Management"])
api_router.include_router(loan.router, tags=["Loan"])
api_router.include_router(strategy.router, tags=["Strategy"])
