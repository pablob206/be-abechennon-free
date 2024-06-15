"""Loan service module"""

# Third-Party
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import logger
from app.data_access import update_add_obj_query
from app.models import Loan
from app.schemas import LoanOperationTypeEnum, LoanRequest, LoanStatusEnum, TradingTypeEnum

# App
from app.service import binance_client


class LoanService:
    """Loan service"""

    def __init__(self, db_session: AsyncSession) -> None:
        """Constructor"""

        self.db_session = db_session

    async def loan_operations(
        self,
        loan_request: LoanRequest,
        loan_operation: LoanOperationTypeEnum,
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
        loan_db = Loan(**loan_request.model_dump())
        loan_db.loan_operation_type = loan_operation
        loan_db.status = LoanStatusEnum.PENDING
        await update_add_obj_query(item=loan_db, db_session=self.db_session)
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
            await update_add_obj_query(item=loan_db, db_session=self.db_session)

        return loan_db
