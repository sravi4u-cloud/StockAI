def quality_score(stock):

    score = 0

    roe = stock.get("roe",0)
    debt = stock.get("debt",1)
    margin = stock.get("margin",0)

    if roe >= 20:
        score += 40

    elif roe >=15:
        score += 25


    if debt == 0:
        score += 30

    elif debt < 0.5:
        score += 15


    if margin >=20:
        score +=30


    return score
def smart_quality_valuation_engine():

    print("\n=== SMART QUALITY & VALUATION ENGINE ===")

    symbol = input("Enter stock symbol: ")

    print(f"\nAnalyzing {symbol}...")
    print("Quality Score Engine Ready")
