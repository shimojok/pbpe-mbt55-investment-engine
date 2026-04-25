def calculate_irr(cashflows):
    rate = 0.1
    for _ in range(100):
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cashflows))
        d_npv = sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cashflows))
        rate -= npv / (d_npv + 1e-6)
    return rate

def compare_irr_lcoa(irr, lcoa):
    """
    投資評価の2軸比較
    """
    return {
        "IRR": irr,
        "LCOA": lcoa,
        "Efficiency Score": irr / lcoa  # 新指標
    }