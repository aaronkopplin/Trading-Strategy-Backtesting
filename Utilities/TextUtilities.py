def convert_price_to_str(price: float) -> str:
    return '${:,.0f}'.format(price)


def format_as_two_decimal_price(price: float):
    if price < 0:
        price = abs(price)
        return '$({:,.2f})'.format(price)
    return '${:,.2f}'.format(price)
