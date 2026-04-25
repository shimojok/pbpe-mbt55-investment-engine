import streamlit as st
import pandas as pd

from simulation import simulate, simulate_country
from pbpe_token import pbpe_value
from fund_model import irr_proxy
from carbon_credit import carbon_value

st.set_page_config(layout="wide")

st.title("🌍 PBPE × MBT55 Investment Dashboard")

# =========================
# トグル
# =========================
M = 1 if st.toggle("MBT55 ON", True) else 0

# =========================
# シミュレーション
# =========================
on = simulate(1)
off = simulate(0)
res = simulate(M)

yield_gain = on["Yield"] - off["Yield"]
cost_reduction = off["Cost"] - on["Cost"]
co2_reduction = off["CO2"] - on["CO2"]

# =========================
# 経済計算
# =========================
pbpe = pbpe_value(yield_gain, co2_reduction, cost_reduction)

carbon = carbon_value(co2_reduction)

irr = irr_proxy(
    cost_reduction,
    carbon,
    yield_gain * 50
)

# =========================
# 🚀 投資判断（最上段）
# =========================
st.markdown("## 🚀 Investment Decision")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Profit Impact", round(cost_reduction, 2))
col2.metric("🌱 Carbon Impact", round(co2_reduction, 2))
col3.metric("📈 Yield Growth", round(yield_gain, 2))

# =========================
# 💠 PBPE
# =========================
st.markdown("## 💠 PBPE Value Engine")

st.metric("PBPE Token", round(pbpe, 2))

# =========================
# ♻️ グリーンプレミアム
# =========================
st.markdown("## ♻️ Negative Green Premium")

st.metric("Cost Advantage", round(cost_reduction, 2))

# =========================
# 💰 カーボン価値
# =========================
st.markdown("## 🌍 Carbon Value")

st.metric("Carbon Revenue ($)", round(carbon, 2))

# =========================
# 💼 投資指標
# =========================
st.markdown("## 💼 Investment Metrics")

col4, col5 = st.columns(2)

col4.metric("IRR Proxy", round(irr, 2))

investment = 200
payback = investment / (cost_reduction + carbon/1000 + yield_gain * 50)

col5.metric("Payback (years)", round(payback, 2))

# =========================
# 🟢 投資判断
# =========================
st.markdown("## 🟢 Investment Signal")

if cost_reduction > 0 and co2_reduction > 0:
    st.success("STRONG BUY")
else:
    st.warning("REVIEW REQUIRED")

# =========================
# 📊 KPI
# =========================
st.markdown("## 📊 Core Metrics")

col6, col7, col8 = st.columns(3)

col6.metric("Yield", round(res["Yield"], 2))
col7.metric("Cost", round(res["Cost"], 2))
col8.metric("CO2", round(res["CO2"], 2))

# =========================
# 📈 ON vs OFF
# =========================
st.markdown("## 📈 ON vs OFF")

df_compare = pd.DataFrame({
    "ON": on,
    "OFF": off
})

st.bar_chart(df_compare)

# =========================
# 🌐 国別展開
# =========================
st.markdown("## 🌐 Global Expansion")

df = pd.read_csv("data/country_coffee_sample.csv")

results = [simulate_country(row, M) for _, row in df.iterrows()]
res_df = pd.DataFrame(results)

st.dataframe(res_df)

st.bar_chart(res_df.set_index("country")[["Yield", "Cost", "CO2"]])

# =========================
# 🔍 信頼性
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
# 🌍 市場規模
# =========================
st.markdown("## 🌍 Market Scale")

global_market = 100_000_000_000

impact_ratio = min(1.0, yield_gain / 3.0)

tam = global_market * impact_ratio

st.metric("Addressable Market ($)", f"{int(tam):,}")

# =========================
# 🧠 Insight
# =========================
st.markdown("## 🧠 Executive Insight")

st.success(
    f"MBT55 enables {round(cost_reduction,0)} cost reduction, "
    f"{round(co2_reduction,0)} CO2 reduction, "
    f"and {round(yield_gain,1)} yield increase simultaneously."
)