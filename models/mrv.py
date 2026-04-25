def calculate_verified_credits(baseline, project, leakage_rate=0.1, buffer_rate=0.2):
    reduction = baseline - project
    reduction = reduction * (1 - leakage_rate)
    reduction = reduction * (1 - buffer_rate)
    return reduction


def calculate_carbon_revenue(verified_credits, carbon_price):
    return verified_credits * carbon_price