"""Order management test layer module"""
# Third-Party
import pytest

# App
from app.service.order_management import OrderManagementService


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (
            0.00071628,
            0.00071,
        ),
        (
            0.0071628,
            0.0071,
        ),
        (
            0.071628,
            0.071,
        ),
        (
            0.71628,
            0.71,
        ),
        (
            3.00071628,
            3.0,
        ),
        (
            3.41071628,
            3.4,
        ),
        (
            33.41071628,
            33.0,
        ),
        (
            333.41071628,
            333.0,
        ),
    ],
)
def test_format_quantity(
    value: float,
    expected_result: float,
):
    """
    Test format_quantity function
    """

    assert OrderManagementService.format_quantity(value=value) == expected_result
