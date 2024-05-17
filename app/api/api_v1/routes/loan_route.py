"""Loan routes module v1"""

# Third-Party
from fastapi import APIRouter, status

# App
from app.service import LoanService
from app.schemas import LoanRequest, LoanOperationTypeEnum
from app.api import DBSessionDep

router = APIRouter()


@router.post(
    path="/loan/create",
    summary="Create Margin Loan",
    response_model_exclude={"id"},
    status_code=status.HTTP_201_CREATED,
)
async def create_loan(loan_request: LoanRequest, db_session: DBSessionDep):
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

    return await LoanService(db_session=db_session).loan_operations(
        loan_request=loan_request,
        loan_operation=LoanOperationTypeEnum.CREATE_MARGIN_LOAN,
    )


@router.post(
    path="/loan/repay",
    summary="Repay Margin Loan",
    response_model_exclude={"id"},
    status_code=status.HTTP_201_CREATED,
)
async def repay_loan(loan_request: LoanRequest, db_session: DBSessionDep):
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

    return await LoanService(db_session=db_session).loan_operations(
        loan_request=loan_request,
        loan_operation=LoanOperationTypeEnum.REPAY_MARGIN_LOAN,
    )
