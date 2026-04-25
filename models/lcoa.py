def calculate_lcoa(capex, opex, yield_series, discount_rate):
    discounted_opex = sum(
        opex[t] / ((1 + discount_rate) ** (t + 1))
        for t in range(len(opex))
    )

    discounted_yield = sum(
        yield_series[t] / ((1 + discount_rate) ** (t + 1))
        for t in range(len(yield_series))
    )

    return (capex + discounted_opex) / discounted_yield