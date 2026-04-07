import streamlit as st
import pandas as pd

from simulation import simulate, simulate_country
from pbpe_token import pbpe_value
from fund_model import irr_proxy
from carbon_credit import carbon_value

st.set_page_config(layout="wide")

st.title("🌍 PBPE × MBT55 Investment Dashboard")

# =========================
# ON/OFF
# =========================
M = 1 if st.toggle("MBT55 ON/OFF", True) else 0

# =========================
# Simulation
# =========================
on = simulate(1)
off = simulate(0)
res = simulate(M)

yield_gain = on["Yield"] - off["Yield"]
cost_reduction = off["Cost"] - on["Cost"]
co2_reduction = off["CO2"] - on["CO2"]

# =========================
# Economics
# =========================
pbpe = pbpe_value(yield_gain, co2_reduction, cost_reduction)
carbon = carbon_value(co2_reduction)
irr = irr_proxy(cost_reduction, carbon, yield_gain * 50)

# =========================
# Investment Decision
# =========================
st.markdown("## 🚀 Investment Decision")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Profit Impact", round(cost_reduction if M else 0, 2))
col2.metric("🌱 Carbon Impact", round(co2_reduction if M else 0, 2))
col3.metric("📈 Yield Growth", round(yield_gain if M else 0, 2))

# =========================
# PBPE
# =========================
st.markdown("## 💠 PBPE Value Engine")
st.metric("PBPE Token", round(pbpe if M else 0, 2))

# =========================
# Green Premium
# =========================
st.markdown("## ♻️ Negative Green Premium")
st.metric("Cost Advantage", round(cost_reduction if M else 0, 2))

# =========================
# Carbon
# =========================
st.markdown("## 🌍 Carbon Value")
st.metric("Carbon Revenue ($)", round(carbon if M else 0, 2))

# =========================
# Investment Metrics
# =========================
st.markdown("## 💼 Investment Metrics")

col4, col5 = st.columns(2)

col4.metric("IRR Proxy", round(irr if M else 0, 2))

investment = 200
payback = investment / max(1, (cost_reduction + carbon/1000 + yield_gain * 50))

col5.metric("Payback (years)", round(payback if M else 0, 2))

# =========================
# Signal
# =========================
st.markdown("## 🟢 Investment Signal")

if M and cost_reduction > 0 and co2_reduction > 0:
    st.success("STRONG BUY")
else:
    st.warning("OFF or REVIEW")

# =========================
# Core Metrics
# =========================
st.markdown("## 📊 Core Metrics")

col6, col7, col8 = st.columns(3)

col6.metric("Yield", round(res["Yield"], 2))
col7.metric("Cost", round(res["Cost"], 2))
col8.metric("CO2", round(res["CO2"], 2))

# =========================
# ON vs OFF（修正済み）
# =========================
st.markdown("## 📈 ON vs OFF")

df_compare = pd.DataFrame({
    "State": ["OFF", "ON"],
    "Yield": [off["Yield"], on["Yield"]],
    "Cost": [off["Cost"], on["Cost"]],
    "CO2": [off["CO2"], on["CO2"]]
})

st.bar_chart(df_compare.set_index("State"))

# =========================
# Country Expansion
# =========================
st.markdown("## 🌐 Global Expansion")

df = pd.read_csv("data/country_coffee_sample.csv")

results = [simulate_country(row, M) for _, row in df.iterrows()]
res_df = pd.DataFrame(results)

st.dataframe(res_df)
st.bar_chart(res_df.set_index("country")[["Yield", "Cost", "CO2"]])

# =========================
# Reliability
# =========================
st.markdown("## 🔍 Reliability Score")

confidence = min(
    100,
    (yield_gain / 3.0) * 30 +
    (co2_reduction / 1000) * 40 +
    (cost_reduction / 500) * 30
)

st.metric("Model Confidence (%)", round(confidence, 1))

# =========================
# Market
# =========================
st.markdown("## 🌍 Market Scale")

global_market = 100_000_000_000
impact_ratio = min(1.0, yield_gain / 3.0)
tam = global_market * impact_ratio

st.metric("Addressable Market ($)", f"{int(tam):,}")

# =========================
# Insight
# =========================
st.markdown("## 🧠 Executive Insight")

st.success(
    f"MBT55 enables {round(cost_reduction,0)} cost reduction, "
    f"{round(co2_reduction,0)} CO2 reduction, "
    f"and {round(yield_gain,1)} yield increase."
)