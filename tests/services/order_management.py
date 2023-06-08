"""Order management test layer module"""
# Third-Party

# App
from app.service.order_management.utils import format_quantity


import pytest
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
    ],
)
def test_format_quantity(
    value: float,
    expected_result: float,
):
    """
    Test format_quantity function
    0.0070628(no admitido) a 0.0070
    """

    assert (
        format_quantity(value=value) == expected_result
    )


