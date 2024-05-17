"""Order management service module"""

# Third-Party
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# App
from app.config import logger
from app.service.binance import binance_client
from app.models import Order
from app.schemas import OrderRequest, TradingTypeEnum
from app.data_access import (
    update_add_obj_query,
    get_orders_query,
)


class OrderManagementService:
    """Order management service"""

    def __init__(self, db_session: AsyncSession) -> None:
        """Constructor"""

        self.db_session = db_session

    async def create_order(self, order: OrderRequest) -> Order:
        """
        Create order (Only MARGIN trading supported)
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
                detail=f"Only [{TradingTypeEnum.MARGIN}] trading supported",
            )

        order_db = Order(**order.model_dump())
        await update_add_obj_query(item=order_db, db_session=self.db_session)

        try:
            order_resp = await binance_client().create_margin_order(
                symbol=order.pair,
                isIsolated=order.is_isolated,
                side=order.side,
                type=order.ord_type,
                quantity=order.orig_qty,
                timeInForce=order.time_in_force,
                price=order.limit_price,
            )
        except Exception as exc:
            logger.error("Failed to create order")
            raise HTTPException(status_code=400, detail=f"Failed to create [{order.trading_type}] order") from exc

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

        return await update_add_obj_query(item=order_db, db_session=self.db_session)

    async def get_orders(self, _id: int | None = None) -> list[Order]:
        """Get orders"""

        if not (orders_db := await get_orders_query(_id=_id, db_session=self.db_session)):
            raise HTTPException(status_code=404, detail="Orders not found")

        return orders_db

    @staticmethod
    def calculate_quantity(amount_per_order: float, close: float) -> float:
        """
        Calculate quantity to buy/sell
        :param amount_per_order: float, amount per order (in quote currency_base). I.e: 20.0
        :param close: float, close price. I.e: 1802.3
        :return: float, quantity to buy/sell. I.e: 0.011096932
        """

        return amount_per_order / close

    @staticmethod
    def format_quantity(value: float) -> float:
        """
        Format quantity
        I.e:
        from 0.00071628 to 0.00071
        from 0.0071628 to 0.0071
        from 0.071628 to 0.071
        from 0.71628 to 0.71
        from 3.00071628 to 3.0
        from 3.41071628 to 3.4
        from 33.41071628 to 33.0
        from 333.41071628 to 333.0
        """

        integer_part: int = int(value)
        if 0 < integer_part < 10:
            return round(value, 1)
        if integer_part >= 10:
            return float(integer_part)

        # flags
        decimal_part_found = False
        first_dig_found = False
        second_dig_found = False

        results = []
        for item in list(str(value)):
            if not decimal_part_found and item != ".":
                results.append(item)
            elif not decimal_part_found and item == ".":
                decimal_part_found = True
                results.append(item)
            elif decimal_part_found and not first_dig_found:
                if (item) > "0":
                    first_dig_found = True
                results.append(item)
            elif first_dig_found and not second_dig_found:
                second_dig_found = True
                results.append(item)

        return float("".join(results))
