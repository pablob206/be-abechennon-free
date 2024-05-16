"""Bot routes"""
# Third-Party
from fastapi import APIRouter

# App
from app.service.binance import (
    get_pairs_availables,
    get_assets_details,
)
from app.service.setting import SettingsService
from app.service.strategy import strategy_temp
from app.schemas import TradingTypeEnum, WalletTypeEnum
from app.api.deps import DBSessionDep
from app.data_access import get_setting_query

router = APIRouter()


@router.get(path="/bot/feat-test")
async def feat_test(db_session: DBSessionDep):
    """
    Endpoint for feature testing
    """

    setting_db = await get_setting_query(db_session=db_session)
    return await strategy_temp(pair="UNIUSDT", setting_db=setting_db)


@router.get(path="/bot/status")
async def get_bot_status(db_session: DBSessionDep):
    """
    Get bot status
    - **:return:** dict, bot status. I.e: \n
            {
                "bot_status": "MAINTANANCE"
            }
    """

    return await SettingsService(db_session=db_session).get_bot_status()


@router.get(path="/{wallet}/assets")
async def get_assets_details(
    db_session: DBSessionDep, wallet: WalletTypeEnum = WalletTypeEnum.MARGIN
):
    """
    Get assets details by wallet
    - **:param wallet:** WalletTypeEnum (Default WalletTypeEnum.MARGIN),
    wallet type. I.e: WalletTypeEnum.MARGIN
    - **:return:** dict. Detail margin account. I.e: \n
            {
                "IOTAUSDT": {
                    "asset": "IOTA",
                    "free": 11.1,
                    "locked": 0.0,
                    "borrowed": 0.0,
                    "interest": 0.0,
                    "netAsset": 11.1,
                    "freeUsdt": 2.11233,
                    "borrowedUsdt": 0.0
                },
                "ALGOUSDT": {
                    "asset": "ALGO",
                    "free": 8.0,
                    "locked": 0.0,
                    "borrowed": 0.0,
                    "interest": 0.0,
                    "netAsset": 8.0,
                    "freeUsdt": 1.3064,
                    "borrowedUsdt": 0.0
                },
                ...
            }
    """

    return await get_assets_details(db_session=db_session, wallet=wallet)


@router.get(path="/{trade_type}/pairs-availables")
async def get_pairs_availables(
    currency_base: str | None = "USDT",
    trading_type: TradingTypeEnum = TradingTypeEnum.MARGIN,
):
    """
    Get pairs availables by currency-base and trading-type, format: 'pair'-'currency'.
    Current length: 232.
    - **:param currency_base:** str (Default USDT), currency base. I.e: "USDT"
    - **:param trading_type:** TradingTypeEnum (Default TradingTypeEnum.MARGIN),
    trading type. I.e: TradingTypeEnum.MARGIN
    - **:return**: dict, pairs availables. I.e: \n
            {
                "XMRUSDT": "XMR",
                "ADAUSDT": "ADA",
                ...
            }
    """

    return await get_pairs_availables(
        currency_base=currency_base, trading_type=trading_type
    )
