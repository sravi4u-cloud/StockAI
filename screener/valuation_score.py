def calculate_score(stock):
    score = 0

    # ROE quality
    if stock["roe"] >= 20:
        score += 25
    elif stock["roe"] >= 15:
        score += 15

    # PE valuation
    if stock["pe"] <= 15:
        score += 25
    elif stock["pe"] <= 25:
        score += 15

    # Growth proxy
    if stock.get("growth",0) >= 15:
        score += 25

    # Balance sheet
    if stock.get("debt",1) == 0:
        score += 25

    return score
