import math

def run_step(state, microbial, M, params):

    # -----------------------------
    # 微生物ダイナミクス（M3）
    # -----------------------------
    X, S = microbial

    mu = params["microbial_growth"]
    decay = params["microbial_decay"]

    dX = mu * X * S - decay * X
    X_new = max(0.01, X + dX)

    S_new = max(0.01, S - params["substrate_utilization"] * X)

    # -----------------------------
    # 土壌制御（MBT効果）
    # -----------------------------
    nutrient = state["nutrient"] + M * params["nutrient_boost"] * X_new
    toxicity = state["toxic"] * (1 - M * params["toxicity_reduction"])
    salinity = state["salinity"] * (1 - M * params["salinity_reset"])

    # -----------------------------
    # 病害
    # -----------------------------
    D = state["D0"] * math.exp(-params["beta"] * M * X_new)

    # -----------------------------
    # 収量
    # -----------------------------
    Y = params["Y0"] * nutrient * (1 - toxicity) * (1 - salinity) * (1 - D)

    # -----------------------------
    # コスト
    # -----------------------------
    cost = (
        params["fertilizer_price"] * (1 - M)
        + params["process_cost_per_ton"] * M
        - params["waste_disposal_cost"] * M
    )

    # -----------------------------
    # CO2
    # -----------------------------
    CO2 = (
        params["incineration_emission"] * (1 - M)
        + params["process_emission"] * M
        - params["carbon_sequestration"] * M
    )

    # =========================
    # 🔥 制約（ここが正しい位置）
    # =========================
    Y = min(Y, 3.0)
    CO2 = max(CO2, -500)
    cost = max(cost, -200)

    # -----------------------------
    # 状態更新
    # -----------------------------
    new_state = {
        "nutrient": nutrient,
        "toxic": toxicity,
        "salinity": salinity,
        "D0": D,
        "waste_input": state["waste_input"]
    }

    # -----------------------------
    # 出力（1つだけ）
    # -----------------------------
    return new_state, (X_new, S_new), {
        "Yield": Y,
        "Cost": cost,
        "CO2": CO2
    }