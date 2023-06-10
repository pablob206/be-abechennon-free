"""Loan Enum module"""
# Built-In
from enum import Enum


class LoanStatusEnum(str, Enum):
    """
    Define different loan status
    """

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    ERROR = "ERROR"


class LoanOperationTypeEnum(str, Enum):
    """
    Define different loan operations type
    """

    CREATE_MARGIN_LOAN = "CREATE_MARGIN_LOAN"
    REPAY_MARGIN_LOAN = "REPAY_MARGIN_LOAN"
