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
    I.e:
    from 0.00071628 to 0.00071
    from 0.0071628 to 0.0071
    from 0.071628 to 0.071
    from 0.71628 to 0.71
    from 3.00071628 to 3.0
    from 3.41071628 to 3.4
    from 33.41071628 to 33.0
    from 333.41071628 to 333.0
    """

    integer_part: int = int(value)
    if 0 < integer_part < 10:
        return round(value, 1)
    if integer_part >= 10:
        return float(integer_part)

    # flags
    decimal_part_found = False
    first_dig_found = False
    second_dig_found = False

    results = []
    for item in list(str(value)):
        if not decimal_part_found and item != ".":
            results.append(item)
        elif not decimal_part_found and item == ".":
            decimal_part_found = True
            results.append(item)
        elif decimal_part_found and not first_dig_found:
            if (item) > "0":
                first_dig_found = True
            results.append(item)
        elif first_dig_found and not second_dig_found:
            second_dig_found = True
            results.append(item)

    return float("".join(results))
