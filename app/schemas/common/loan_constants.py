"""Module to store loan constants used in the project"""

# Built-In
from enum import StrEnum


class LoanStatusEnum(StrEnum):
    """
    Define different loan status types
    """

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    ERROR = "ERROR"


class LoanOperationTypeEnum(StrEnum):
    """
    Define different loan operations types
    """

    CREATE_MARGIN_LOAN = "CREATE_MARGIN_LOAN"
    REPAY_MARGIN_LOAN = "REPAY_MARGIN_LOAN"
