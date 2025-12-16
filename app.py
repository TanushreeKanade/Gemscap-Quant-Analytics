import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from storage.db import initialize_db, fetch_ticks
from ingestion.binance_ws import start_ingestion

from analytics.resampling import ticks_to_dataframe, resample_ticks
from analytics.regression import align_pairs, compute_hedge_ratio
from analytics.spread import compute_spread, compute_zscore
from analytics.correlation import compute_rolling_correlation
from analytics.stationarity import adf_test
from analytics.halflife import compute_half_life
from analytics.backtest import simple_mean_reversion_backtest



# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="GemsCap Quant Analytics",
    layout="wide"
)

st.title("Real-Time Pair Trading Analytics")


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------
initialize_db()


# --------------------------------------------------
# Start WebSocket Ingestion (once per session)
# --------------------------------------------------
if "ingestion_started" not in st.session_state:
    symbols = ["btcusdt", "ethusdt"]
    start_ingestion(symbols)
    st.session_state.ingestion_started = True
    st.success("Binance WebSocket ingestion started")


# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------
st.sidebar.header("Controls")

timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["1s", "1m", "5m"],
    key="timeframe"
)

rolling_window = st.sidebar.slider(
    "Rolling Window",
    min_value=10,
    max_value=200,
    value=30,
    key="rolling_window"
)

alert_threshold = st.sidebar.slider(
    "Z-Score Alert Threshold",
    min_value=1.0,
    max_value=3.0,
    value=2.0,
    key="alert_threshold"
)


# --------------------------------------------------
# Fetch Tick Data
# --------------------------------------------------
rows_a = fetch_ticks("btcusdt")
rows_b = fetch_ticks("ethusdt")

if len(rows_a) < rolling_window or len(rows_b) < rolling_window:
    st.warning("Collecting data... please wait.")
    st.stop()


# --------------------------------------------------
# Resampling
# --------------------------------------------------
df_a = resample_ticks(
    ticks_to_dataframe(rows_a),
    timeframe
)

df_b = resample_ticks(
    ticks_to_dataframe(rows_b),
    timeframe
)


# --------------------------------------------------
# Cached Analytics Pipeline
# --------------------------------------------------
@st.cache_data(ttl=5)
def compute_all_metrics(df_a, df_b, rolling_window):
    aligned = align_pairs(df_a, df_b)
    beta, alpha = compute_hedge_ratio(aligned)
    spread = compute_spread(aligned, beta)
    zscore = compute_zscore(spread, rolling_window)
    corr = compute_rolling_correlation(aligned, rolling_window)
    return aligned, beta, spread, zscore, corr


aligned, beta, spread, zscore, corr = compute_all_metrics(
    df_a, df_b, rolling_window
)


# --------------------------------------------------
# Scalar Values for Interpretation & Alerts
# --------------------------------------------------
latest_z = zscore.iloc[-1]
latest_corr = corr.iloc[-1]

adf_result = adf_test(spread)
adf_p = adf_result["p_value"]

half_life = compute_half_life(spread)

backtest_df = simple_mean_reversion_backtest(
    spread,
    zscore,
    entry=alert_threshold
)
####


# --------------------------------------------------
# Key Metrics
# --------------------------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Hedge Ratio (β)", f"{beta:.4f}")
col2.metric("Latest Z-Score", f"{latest_z:.2f}")
col3.metric("Latest Correlation", f"{latest_corr:.2f}")

if half_life:
    col4.metric("Mean Reversion Half-Life", f"{half_life} periods")
else:
    col4.metric("Mean Reversion Half-Life", "N/A")


# --------------------------------------------------
# Quant Interpretation
# --------------------------------------------------
st.subheader("Quant Interpretation")

interpretation = []

interpretation.append(
    "• Spread deviation is statistically significant"
    if abs(latest_z) >= alert_threshold
    else "• Spread deviation is within normal range"
)

interpretation.append(
    "• Correlation remains strong, pair relationship intact"
    if latest_corr >= 0.5
    else "• Correlation is weak, hedge reliability may be reduced"
)

interpretation.append(
    f"• Spread appears stationary (ADF p-value = {adf_p:.4f})"
    if adf_p < 0.05
    else f"• No strong evidence of stationarity (ADF p-value = {adf_p:.4f})"
)

if half_life:
    interpretation.append(
        f"• Estimated mean-reversion half-life: {half_life} periods"
    )

for line in interpretation:
    st.write(line)


# --------------------------------------------------
# Trader Interpretation Panel
# --------------------------------------------------
st.subheader("📊 Trader Interpretation")

if abs(latest_z) > 2 and adf_p < 0.05 and latest_corr > 0.7:
    st.success(
        f"""
        **Market State:** Mean Reversion Candidate  

        • Spread deviation: {latest_z:.2f}σ  
        • Cointegration confirmed (ADF p-value: {adf_p:.4f})  
        • Rolling correlation: {latest_corr:.2f}  
        • Estimated half-life: {half_life} periods  

        **Trade Bias:** Look for spread reversion  
        **Risk:** Correlation breakdown or regime shift
        """
    )
else:
    st.info(
        f"""
        **Market State:** No Strong Signal  

        • Z-score: {latest_z:.2f}  
        • ADF p-value: {adf_p:.4f}  
        • Correlation: {latest_corr:.2f}  

        **Bias:** Stay neutral
        """
    )


# backtest
st.subheader("📈 Mini Mean-Reversion Backtest")

st.dataframe(
    backtest_df.tail(15),
    use_container_width=True
)

st.metric(
    "Cumulative PnL",
    f"{backtest_df['PnL'].sum():.4f}"
)



# --------------------------------------------------
# Limit Plot Size
# --------------------------------------------------
MAX_POINTS = 300

st.subheader("Price Series")
st.line_chart(aligned.tail(MAX_POINTS)[["price_a", "price_b"]])

st.subheader("Spread")
st.line_chart(spread.tail(MAX_POINTS))

st.subheader("Z-Score (Regime Highlighted)")

z_plot = zscore.tail(MAX_POINTS)
threshold = alert_threshold

fig = go.Figure()

# Z-score line
fig.add_trace(
    go.Scatter(
        y=z_plot,
        mode="lines",
        name="Z-Score"
    )
)

# Upper threshold
fig.add_hline(
    y=threshold,
    line_dash="dash",
    line_color="red",
    annotation_text="+Threshold"
)

# Lower threshold
fig.add_hline(
    y=-threshold,
    line_dash="dash",
    line_color="green",
    annotation_text="-Threshold"
)

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=30, b=20),
    yaxis_title="Z-Score",
    xaxis_title="Time"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Rolling Correlation")
st.line_chart(corr.tail(MAX_POINTS))


# --------------------------------------------------
# Alerts
# --------------------------------------------------
if abs(latest_z) >= alert_threshold:
    st.error(
        f"""
        🚨 **Trading Alert Triggered**

        • Z-score: {latest_z:.2f}  
        • Correlation: {latest_corr:.2f}  
        • ADF p-value: {adf_p:.4f}
        """
    )


# --------------------------------------------------
# Export Analytics
# --------------------------------------------------
export_df = pd.DataFrame({
    "spread": spread,
    "zscore": zscore,
    "correlation": corr
})

st.download_button(
    label="Download Analytics CSV",
    data=export_df.to_csv().encode("utf-8"),
    file_name="analytics_output.csv",
    mime="text/csv"
)
