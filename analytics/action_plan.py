from analytics.valuation_recommendation import get_valuation_recommendations
from analytics.fair_value_engine import get_fair_value_recommendations

def get_action_plan():
    quality_data = {r["symbol"]: r for r in get_valuation_recommendations()}
    fair_value_data = {r["symbol"]: r for r in get_fair_value_recommendations()}

    keep = []
    add = []
    reduce = []
    exit_stocks = []

    for symbol, q in quality_data.items():
        f = fair_value_data.get(symbol, {})
        score = q.get("score", 0)
        upside = f.get("upside", 0)
        confidence = f.get("confidence", 0)

        # Decision logic
        if score >= 65 and upside > 10 and confidence >= 70:
            add.append({
                "symbol": symbol,
                "score": score,
                "upside": upside,
                "reason": "High quality with strong upside"
            })

        elif score >= 55:
            keep.append({
                "symbol": symbol,
                "score": score,
                "upside": upside,
                "reason": "Strong core holding"
            })

        elif score >= 40:
            reduce.append({
                "symbol": symbol,
                "score": score,
                "upside": upside,
                "reason": "Moderate quality, reduce gradually"
            })

        else:
            exit_stocks.append({
                "symbol": symbol,
                "score": score,
                "upside": upside,
                "reason": "Weak quality, exit first"
            })

    # Sort each category
    add = sorted(add, key=lambda x: x["score"], reverse=True)[:10]
    keep = sorted(keep, key=lambda x: x["score"], reverse=True)[:10]
    reduce = sorted(reduce, key=lambda x: x["score"])[:10]
    exit_stocks = sorted(exit_stocks, key=lambda x: x["score"])[:10]

    return {
        "KEEP": keep,
        "ADD": add,
        "REDUCE": reduce,
        "EXIT": exit_stocks
    }