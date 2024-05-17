"""Order management routes module v1"""

# Third-Party
from fastapi import APIRouter, status

# App
from app.service import OrderManagementService
from app.schemas import OrderRequest
from app.api import DBSessionDep

router = APIRouter()


@router.post(
    path="/order",
    summary="Create new order",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_order(order: OrderRequest, db_session: DBSessionDep):
    """
    Create new order (only available for MARGIN trading type)
    - **:Request body:** \n
            {
                "pair": (str) pair symbol. I.e: "BTCUSDT",
                "trading_type": (TradingTypeEnum[str]) trading type.
                I.e: "SPOT" | "MARGIN" | "FUTURES",
                "is_isolated": (bool) is isolated. I.e: False,
                "side": (SideEnum[str]) order side. I.e: "BUY" | "SELL",
                "ord_type": (OrdTypeEnum[str]) order type. I.e: "LIMIT" | "MARKET",
                "orig_qty": (float) quantity. I.e: 1.36,
                "time_in_force": (TimeInForceEnum[str]) time in force. I.e: "GTC" | "IOC" | "FOK" ,
                "limit_price": (float) limit price. I.e: 1802.30
            }
    - **:return:** Order, order info. I.e: \n
            {
                "id": 9,
                "pair": "BTCUSDT",
                "trading_type": "MARGIN",
                "order_id": 28,
                "client_order_id": "6gCrw2kRUAF9CvJDGP16IP",
                "transact_time": 1507725176595,
                "price": "1.00000000",
                "orig_qty": 1.36,
                "executed_qty": "10.00000000",
                "cummulative_quote_qty": "10.00000000",
                "status": "FILLED",
                "time_in_force": "GTC",
                "ord_type": "MARKET",
                "side": "BUY",
                "margin_buy_borrow_amount": 5,
                "margin_buy_borrow_asset": "BTC",
                "is_isolated": false,
                "created_at": "2023-06-07T17:22:37.063871",
                "updated_at": "2023-06-07T17:22:42.078736",
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
                    }
                ]
            }
    """

    return await OrderManagementService(db_session=db_session).create_order(order=order)


@router.get(
    path="/orders",
    summary="Get orders",
    status_code=status.HTTP_200_OK,
)
async def get_orders(db_session: DBSessionDep, _id: int | None = None):
    """
    Get orders by _id, or all orders (_id = None)
    - **:param _id:** (int, Optional), order id. I.e: 7
    - **:return:** List[Order], list of order. I.e: \n
            [
                {
                    "pair": "BTCUSDT",
                    "trading_type": "MARGIN",
                    "order_id": 28,
                    "client_order_id": "6gCrw2kRUAF9CvJDGP16IP",
                    "price": 28002.3,
                    "limit_price": null,
                    "side": "BUY",
                    ...
                },
                {
                    "pair": "ETHUSDT",
                    "trading_type": "MARGIN",
                    "order_id": 29,
                    "client_order_id": "2grw2kRU12favJDG5hgfUH,
                    "price": 1802.3,
                    "limit_price": null,
                    "side": "BUY",
                    ...
                },
                ...
            ]
    """

    return await OrderManagementService(db_session=db_session).get_orders(_id=_id)
