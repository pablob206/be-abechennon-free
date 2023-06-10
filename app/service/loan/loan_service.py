"""Loan service module"""
# Third-Party
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# App
from app.service.binance import binance_client
from app.models import Loan, TradingTypeEnum, LoanOperationTypeEnum, LoanStatusEnum
from app.schemas import LoanSchema
from app.config import logger
from app.data_access import update_add_obj_query


async def loan_operations(
    loan_request: LoanSchema,
    loan_operation: LoanOperationTypeEnum,
    db_session: AsyncSession,
) -> Loan:
    """
    Loan operations (only MARGIN trading supported)
    Binance api client response. I.e: loan_operation = {"tranId": 138386190154, "clientTag": ""}
    """

    if loan_request.trading_type != TradingTypeEnum.MARGIN:
        raise HTTPException(
            status_code=400,
            detail=f"Only [{TradingTypeEnum.MARGIN}] trading supported",
        )
    loan_db = Loan(**loan_request.dict())
    loan_db.loan_operation_type = loan_operation
    loan_db.status = LoanStatusEnum.PENDING
    await update_add_obj_query(item=loan_db, db_session=db_session)
    try:
        loan_resp = await getattr(binance_client(), loan_operation.lower())(
            asset=loan_request.asset, amount=loan_request.amount
        )
        loan_db.status = LoanStatusEnum.APPROVED
        loan_db.tran_id = loan_resp.get("tranId")
        loan_db.client_tag = loan_resp.get("clientTag")
    except Exception as exc:
        loan_db.status = LoanStatusEnum.ERROR
        logger.exception(exc)
        raise HTTPException(
            status_code=400,
            detail=f"Error creating loan: {exc}",
        ) from exc
    finally:
        await update_add_obj_query(item=loan_db, db_session=db_session)

    return loan_db
