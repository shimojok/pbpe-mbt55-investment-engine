def carbon_credit(soc_before, soc_after, leakage, verify):
    net = soc_after - soc_before
    adjusted = net * (1 - leakage)
    return adjusted * verify
