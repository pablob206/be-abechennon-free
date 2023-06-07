"""Order management service module"""
# Third-Party
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# App
from app.service.binance import binance_client
from app.models import Order, TradingTypeEnum
from app.schemas import OrderSchema
from app.data_access import (
    update_add_obj_query,
    get_orders_query,
)


async def create_order(order: OrderSchema, db_session: AsyncSession) -> Order:
    """
    Create order
    order_resp = {
        "symbol": "BTCUSDT",
        "orderId": 28,
        "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
        "transactTime": 1507725176595,
        "price": "1.00000000",
        "origQty": "10.00000000",
        "executedQty": "10.00000000",
        "cummulativeQuoteQty": "10.00000000",
        "status": "FILLED",
        "timeInForce": "GTC",
        "type": "MARKET",
        "side": "BUY",
        "marginBuyBorrowAmount": 5,
        "marginBuyBorrowAsset": "BTC",
        "isIsolated": True,
        "fills": [
            {
                "price": "4000.00000000",
                "qty": "1.00000000",
                "commission": "4.00000000",
                "commissionAsset": "USDT"
            },
            {
                "price": "3999.00000000",
                "qty": "5.00000000",
                "commission": "19.99500000",
                "commissionAsset": "USDT"
            },
        ]
    }
    """

    if order.trading_type != TradingTypeEnum.MARGIN:
        raise HTTPException(
            status_code=400,
            detail=f"Only [{TradingTypeEnum.MARGIN}] trading is supported",
        )

    order_db = Order(**order.dict())
    await update_add_obj_query(item=order_db, db_session=db_session)

    if not (
        order_resp := binance_client().create_margin_order(
            symbol=order.pair,
            isIsolated=order.is_isolated,
            side=order.side,
            type=order.ord_type,
            quantity=order.orig_qty,
            timeInForce=order.time_in_force,
            price=order.limit_price,
        )
    ):
        raise HTTPException(
            status_code=400, detail=f"Failed to create [{order.trading_type}] order"
        )

    order_db.order_id = order_resp.get("orderId")
    order_db.client_order_id = order_resp.get("clientOrderId")
    order_db.transact_time = order_resp.get("transactTime")
    order_db.price = order_resp.get("price")
    order_db.executed_qty = order_resp.get("executedQty")
    order_db.cummulative_quote_qty = order_resp.get("cummulativeQuoteQty")
    order_db.status = order_resp.get("status")
    order_db.time_in_force = order_resp.get("timeInForce")
    order_db.margin_buy_borrow_amount = order_resp.get("marginBuyBorrowAmount")
    order_db.margin_buy_borrow_asset = order_resp.get("marginBuyBorrowAsset")
    order_db.fills = order_resp.get("fills")

    return await update_add_obj_query(item=order_db, db_session=db_session)


async def get_orders(db_session: AsyncSession, _id: int | None = None) -> list[Order]:
    """
    Get orders
    """

    if not (orders_db := await get_orders_query(_id=_id, db_session=db_session)):
        raise HTTPException(404, "Orders not found")
    return orders_db
