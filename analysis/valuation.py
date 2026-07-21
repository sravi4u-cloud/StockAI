def graham_intrinsic_value(eps, growth_rate):
    """
    Calculate intrinsic value using Graham Formula.
    """
    intrinsic_value = eps * (8.5 + 2 * growth_rate)
    return round(intrinsic_value, 2)

def dcf_valuation(fcf, growth_rate, discount_rate, terminal_growth, shares_outstanding):
    """
    Calculate intrinsic value per share using a simple 5-year DCF model.

    fcf: Current Free Cash Flow
    growth_rate: Expected annual growth rate (%)
    discount_rate: Discount rate / WACC (%)
    terminal_growth: Terminal growth rate (%)
    shares_outstanding: Total shares outstanding
    """

    growth_rate /= 100
    discount_rate /= 100
    terminal_growth /= 100

    projected_fcf = []
    present_value = 0

    current_fcf = fcf

    # Project FCF for 5 years
    for year in range(1, 6):
        current_fcf *= (1 + growth_rate)
        projected_fcf.append(current_fcf)

        pv = current_fcf / ((1 + discount_rate) ** year)
        present_value += pv

    # Terminal value
    terminal_value = (
        projected_fcf[-1] * (1 + terminal_growth)
    ) / (discount_rate - terminal_growth)

    terminal_pv = terminal_value / ((1 + discount_rate) ** 5)

    enterprise_value = present_value + terminal_pv

    intrinsic_value_per_share = enterprise_value / shares_outstanding

    return round(intrinsic_value_per_share, 2)