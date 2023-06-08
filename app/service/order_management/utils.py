"""Order management utilities module"""


def calculate_quantity(amount_per_order: float, close: float) -> float:
    """
    Calculate quantity to buy/sell
    :param amount_per_order: float, amount per order (in quote currency_base). I.e: 20.0
    :param close: float, close price. I.e: 1802.3
    :return: float, quantity to buy/sell. I.e: 0.011096932
    """

    return amount_per_order / close


def format_quantity(value: float) -> float:
    """
    Format quantity
    """

    return
