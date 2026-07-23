def investment_view(total_score):

    if total_score >=80:
        return "STRONG BUY"

    elif total_score >=60:
        return "BUY"

    elif total_score >=40:
        return "HOLD"

    else:
        return "AVOID"
