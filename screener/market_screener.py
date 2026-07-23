from screener.valuation_score import calculate_score
from database.db_manager import save_screener_result


def screen_stock(stock):

    score = calculate_score(stock)

    stock["score"] = score

    save_screener_result(stock)

    return stock


def run_screener(stock_list):

    results=[]

    for stock in stock_list:
        results.append(screen_stock(stock))

    return sorted(
        results,
        key=lambda x:x["score"],
        reverse=True
    )
