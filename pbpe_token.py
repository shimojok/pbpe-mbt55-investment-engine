def pbpe_value(yield_gain, co2_reduction, cost_reduction):
    return (
        yield_gain * 100
        + co2_reduction * 0.5
        + cost_reduction * 0.3
    )