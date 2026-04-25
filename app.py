import streamlit as st
import numpy_financial as npf

from models.lcoa import calculate_lcoa
from models.mrv import calculate_verified_credits, calculate_carbon_revenue
from models.token_model import simulate_token_price

st.set_page_config(layout="wide")

st.title("PBPE × MBT55 Investment Dashboard")

# =========================
# ■ INPUT
# =========================
mbt_on = st.sidebar.checkbox("MBT55 ON", value=True)

capex = st.sidebar.number_input("CAPEX", value=1000.0)
opex_base = st.sidebar.number_input("OPEX/year", value=100.0)
discount_rate = st.sidebar.slider("Discount Rate", 0.0, 0.3, 0.1)

baseline_emission = st.sidebar.number_input("Baseline CO2", value=1000.0)
project_emission = st.sidebar.number_input("Project CO2", value=600.0)
carbon_price = st.sidebar.number_input("Carbon Price", value=30.0)

token_price = st.sidebar.number_input("Initial Token Price", value=10.0)

# =========================
# ■ DYNAMIC MODEL（簡易）
# =========================
T = 10
soil = [1.0]
yield_series = []
opex = []

for t in range(T):
    if mbt_on:
        delta_soc = 0.05
        yield_boost = 0.5
        cost_reduction = 0.02
        emission_reduction = 1.0
    else:
        delta_soc = 0.01
        yield_boost = 0.2
        cost_reduction = 0.0
        emission_reduction = 0.0

    soil.append(soil[-1] + delta_soc)

    y = 3 + yield_boost * soil[-1]
    yield_series.append(y)

    opex.append(opex_base * (1 - cost_reduction * t))

# =========================
# ■ CALCULATIONS
# =========================
def run_model(mbt_on_flag):
    soil = [1.0]
    yield_series = []
    opex = []

    for t in range(T):
        if mbt_on_flag:
            delta_soc = 0.05
            yield_boost = 0.5
            cost_reduction = 0.02
            emission_factor = 0.7
        else:
            delta_soc = 0.01
            yield_boost = 0.2
            cost_reduction = 0.0
            emission_factor = 1.0

        soil.append(soil[-1] + delta_soc)

        y = 3 + yield_boost * soil[-1]
        yield_series.append(y)

        opex.append(opex_base * (1 - cost_reduction * t))

    lcoa_val = calculate_lcoa(capex, opex, yield_series, discount_rate)

    price_per_unit = 200
    cash_flows = [-capex] + [y * price_per_unit - o for y, o in zip(yield_series, opex)]

    import numpy_financial as npf
    irr_val = npf.irr(cash_flows)

    adjusted_project = project_emission * emission_factor

    verified_val = calculate_verified_credits(baseline_emission, adjusted_project)
    revenue_val = calculate_carbon_revenue(verified_val, carbon_price)

    return lcoa_val, irr_val, verified_val, revenue_val

lcoa_on, irr_on, co2_on, rev_on = run_model(True)
lcoa_off, irr_off, co2_off, rev_off = run_model(False)

def improvement(new, old, reverse=False):
    if old == 0 or old is None:
        return 0

    change = (new - old) / abs(old) * 100

    # コスト系は符号を反転（下がるほど良い）
    if reverse:
        change = -change

    return change

# LCOA
lcoa = calculate_lcoa(capex, opex, yield_series, discount_rate)

# IRR（簡易）
price_per_unit = 200  # ← ここを追加（作物価格）

cash_flows = [-capex] + [
    y * price_per_unit - o
    for y, o in zip(yield_series, opex)
]

irr = npf.irr(cash_flows)

# MRV
if mbt_on:
    adjusted_project_emission = project_emission * 0.7
else:
    adjusted_project_emission = project_emission

verified = calculate_verified_credits(
    baseline_emission,
    adjusted_project_emission
)
carbon_revenue = calculate_carbon_revenue(verified, carbon_price)

# Token（実体連動）
demand = carbon_revenue / 1000
supply = capex / 100

prices = simulate_token_price(
    P0=token_price,
    demand=demand,
    supply=supply
)

# =========================
# ■ KPI表示（ここがスカスカ解消）
# =========================

st.subheader(f"MBT55 Status: {'ON' if mbt_on else 'OFF'}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("LCOA", round(lcoa_on, 2),
            f"{improvement(lcoa_on, lcoa_off, reverse=True):.1f}%")

col2.metric("IRR", round(irr_on, 3),
            f"{improvement(irr_on, irr_off):.1f}%")

col3.metric("CO2 Reduction", round(co2_on, 2),
            f"{improvement(co2_on, co2_off):.1f}%")

col4.metric("Carbon Revenue", round(rev_on, 2),
            f"{improvement(rev_on, rev_off):.1f}%")

# =========================
# ■ GRAPHS
# =========================

st.subheader("Token Price Simulation")
st.line_chart(prices)

col8, col9 = st.columns(2)

with col8:
    st.subheader("Yield Evolution")
    st.line_chart(yield_series)

with col9:
    st.subheader("Soil (SOC) Evolution")
    st.line_chart(soil)

# =========================
# ■ CASHFLOW表示
# =========================
st.subheader("Cash Flow")
st.bar_chart(cash_flows)

# =========================
# ■ LOG（監査）
# =========================
if st.checkbox("Show MRV Log"):
    st.json({
        "baseline": baseline_emission,
        "project": project_emission,
        "verified": verified,
        "carbon_price": carbon_price,
        "revenue": carbon_revenue
    })