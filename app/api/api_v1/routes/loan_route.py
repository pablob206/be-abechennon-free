"""Loan routes module"""
# Third-Party
from fastapi import APIRouter, status

# App
from app.service.loan import loan_operations
from app.models import Loan, LoanOperationTypeEnum
from app.schemas import LoanSchema
from app.api import DBSessionDep

router = APIRouter()


@router.post(
    path="/loan/create",
    summary="Create Margin Loan",
    response_model=Loan,
    response_model_exclude={"id"},
    status_code=status.HTTP_201_CREATED,
)
async def _create_loan(loan_request: LoanSchema, db_session: DBSessionDep):
    """
    Create margin loan (only available for MARGIN trading type) \n
    - **:Request body:** \n
            {
                "asset": (str) asset symbol. I.e: "USDT",
                "amount": (float) amount to loan. I.e: 20.0,
                "trading_type": (TradingTypeEnum[str]) trading type.
                    I.e: "MARGIN" | "FUTURES",
            }
    - **:return:** Loan, loan info. I.e: \n
            {
                "asset": "USDT",
                "amount": 20,
                "trading_type": "MARGIN",
                "status": "APPROVED",
                "tran_id": 138472451941,
                "client_tag": "",
                "loan_operation_type": "CREATE_MARGIN_LOAN",
                "created_at": "2023-06-10T13:32:15.550985",
                "updated_at": "2023-06-10T13:32:15.550991",
            }
    """

    return await loan_operations(
        loan_request=loan_request,
        loan_operation=LoanOperationTypeEnum.CREATE_MARGIN_LOAN,
        db_session=db_session,
    )


@router.post(
    path="/loan/repay",
    summary="Repay Margin Loan",
    response_model=Loan,
    response_model_exclude={"id"},
    status_code=status.HTTP_201_CREATED,
)
async def _repay_loan(loan_request: LoanSchema, db_session: DBSessionDep):
    """
    Repay margin loan (only available for MARGIN trading type) \n
    - **:Request body:** \n
            {
                "asset": (str) asset symbol. I.e: "USDT",
                "amount": (float) amount to loan. I.e: 20.0,
                "trading_type": (TradingTypeEnum[str]) trading type.
                    I.e: "MARGIN" | "FUTURES",
            }
    - **:return:** Loan, loan info. I.e: \n
            {
                "asset": "USDT",
                "amount": 20,
                "trading_type": "MARGIN",
                "status": "APPROVED",
                "tran_id": 138472451941,
                "client_tag": "",
                "loan_operation_type": "REPAY_MARGIN_LOAN",
                "created_at": "2023-06-10T13:32:15.550985",
                "updated_at": "2023-06-10T13:32:15.550991",
            }
    """

    return await loan_operations(
        loan_request=loan_request,
        loan_operation=LoanOperationTypeEnum.REPAY_MARGIN_LOAN,
        db_session=db_session,
    )
