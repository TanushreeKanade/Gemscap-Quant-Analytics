import streamlit as st
import pandas as pd

from storage.db import initialize_db, fetch_ticks
from ingestion.binance_ws import start_ingestion

from analytics.resampling import ticks_to_dataframe, resample_ticks
from analytics.regression import align_pairs, compute_hedge_ratio
from analytics.spread import compute_spread, compute_zscore
from analytics.correlation import compute_rolling_correlation
from analytics.stationarity import adf_test


# Page Configuration
st.set_page_config(
    page_title="GemsCap Quant Analytics",
    layout="wide"
)

st.title("Real-Time Pair Trading Analytics")


# Initialize Database
initialize_db()

# Start WebSocket Ingestion (once per session)
if "ingestion_started" not in st.session_state:
    symbols = ["btcusdt", "ethusdt"]
    start_ingestion(symbols)
    st.session_state.ingestion_started = True
    st.success("Binance WebSocket ingestion started")

# Sidebar Controls (session-safe)
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

# Fetch Tick Data
rows_a = fetch_ticks("btcusdt")
rows_b = fetch_ticks("ethusdt")

if len(rows_a) < rolling_window or len(rows_b) < rolling_window:
    st.warning("Collecting data... please wait.")
    st.stop()

# Resampling
df_a = resample_ticks(
    ticks_to_dataframe(rows_a),
    timeframe
)

df_b = resample_ticks(
    ticks_to_dataframe(rows_b),
    timeframe
)


# Cached Analytics Pipeline
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


# Key Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Hedge Ratio (β)", f"{beta:.4f}")
col2.metric("Latest Z-Score", f"{zscore.iloc[-1]:.2f}")
col3.metric("Latest Correlation", f"{corr.iloc[-1]:.2f}")

st.subheader("Quant Interpretation")

interpretation = []

# Z-score interpretation
if abs(zscore.iloc[-1]) >= alert_threshold:
    interpretation.append(
        f"• Spread deviation is statistically significant (|Z| ≥ {alert_threshold})"
    )
else:
    interpretation.append(
        "• Spread deviation is within normal range"
    )

# Correlation interpretation
if corr.iloc[-1] < 0.5:
    interpretation.append(
        "• Correlation is weak, hedge reliability may be reduced"
    )
else:
    interpretation.append(
        "• Correlation remains strong, pair relationship intact"
    )

# Stationarity interpretation (ADF)
adf_result = adf_test(spread)
if adf_result["p_value"] < 0.05:
    interpretation.append(
        #f"• Spread appears stationary (ADF p-value = {adf_result['p_value']:.4f})"
        f"• Spread appears stationary (ADF p-value < 0.001)"

    )
else:
    interpretation.append(
        f"• No strong evidence of stationarity (ADF p-value = {adf_result['p_value']:.4f})"
    )

for line in interpretation:
    st.write(line)



# Limit Plot Size for UI Stability
MAX_POINTS = 300

aligned_plot = aligned.tail(MAX_POINTS)
spread_plot = spread.tail(MAX_POINTS)
zscore_plot = zscore.tail(MAX_POINTS)
corr_plot = corr.tail(MAX_POINTS)


# Visualizations
st.subheader("Price Series")
st.line_chart(aligned_plot[["price_a", "price_b"]])

st.subheader("Spread")
st.line_chart(spread_plot)

st.subheader("Z-Score")
st.line_chart(zscore_plot)

st.subheader("Rolling Correlation")
st.line_chart(corr_plot)


# Alerts
if abs(zscore.iloc[-1]) >= alert_threshold:
    st.error(f"ALERT: Z-Score crossed ±{alert_threshold}")


# Export Analytics
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
