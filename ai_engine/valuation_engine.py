def calculate_fair_value(stock):
    """
    Safer intrinsic value model
    """

    price = stock.get("price", 0)
    eps = stock.get("eps", 0)
    growth = stock.get("growth", 0)

    # If EPS is zero or negative, return current price
    if eps <= 0:
        return price

    # Cap growth between 0% and 25%
    growth = max(0, min(growth, 25))

    # Reasonable PE multiple
    pe_multiple = 15 + (growth * 0.4)

    fair_value = eps * pe_multiple

    # Prevent unrealistic values
    if fair_value < price * 0.5:
        fair_value = price * 0.8

    return round(fair_value, 2)