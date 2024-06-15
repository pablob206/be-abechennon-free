"""Api routes"""

# Third-Party
from fastapi import APIRouter

import app.api.api_v1.routes.bot_route as bot
import app.api.api_v1.routes.loan_route as loan
import app.api.api_v1.routes.order_management_route as order_management

# App
import app.api.api_v1.routes.root_route as root
import app.api.api_v1.routes.setting_route as setting
import app.api.api_v1.routes.strategy_route as strategy

api_router = APIRouter()

api_router.include_router(router=root.router, tags=["Info"])
api_router.include_router(router=setting.router, tags=["Setting"])
api_router.include_router(router=bot.router, tags=["Bot"])
api_router.include_router(router=order_management.router, tags=["Order Management"])
api_router.include_router(router=loan.router, tags=["Loan"])
api_router.include_router(router=strategy.router, tags=["Strategy"])
