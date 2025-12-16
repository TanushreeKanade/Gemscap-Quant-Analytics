# Real-Time Pair Trading Analytics Platform  
**GemsCap – Quant Developer Evaluation (Round 1)**

---

## Overview

This project implements a **real-time quantitative analytics platform for statistical pair trading** using live market data streamed from the Binance WebSocket API.

The application demonstrates a **complete end-to-end workflow** — from real-time data ingestion and persistent storage to time-series processing, statistical analytics, interactive visualization, alerting, and lightweight strategy validation.

The system is intentionally designed to emphasize **quantitative reasoning, architectural clarity, and trader-oriented interpretation**, rather than synthetic signals or hardcoded outputs.

---

## Key Capabilities

### Real-Time Data Ingestion
- Live tick-level trade data streamed via Binance WebSocket
- Continuous ingestion for BTCUSDT and ETHUSDT
- Non-blocking ingestion to ensure smooth UI updates

### Persistent Storage
- All tick data is stored in a local SQLite database
- Enables reproducibility, resampling, and offline analysis
- Database is auto-created on first run

### Time-Series Processing
- Tick data is resampled into configurable timeframes:
  - 1 second
  - 1 minute
  - 5 minutes

### Pair Trading Analytics
- OLS-based hedge ratio (β) estimation
- Spread construction using hedge ratio
- Rolling Z-score of the spread
- Rolling correlation between paired assets
- Augmented Dickey-Fuller (ADF) test for stationarity
- Mean-reversion half-life estimation
- Lightweight rule-based mean-reversion backtest

### Interactive Dashboard
- Near real-time analytics updates
- Adjustable rolling window size
- User-defined Z-score alert thresholds
- Z-score regime visualization with threshold highlighting
- Trader interpretation layer translating analytics into actionable insights
- CSV export of processed analytics
- Interactive charts with zoom, pan, and hover

---

## Architecture Overview


```
Binance WebSocket
        │
        ▼
Ingestion Layer (binance_ws.py)
        │
        ▼
SQLite Database (market_data.db)
        │
        ▼
Analytics Layer
(resampling, regression, spread,
 correlation, stationarity)
        │
        ▼
Streamlit Dashboard & Orchestration Layer (app.py)
        │
        ▼
Alerts & Data Export
```


The architecture is modular and loosely coupled, enabling:
- Easy integration of alternate data sources
- Addition of new analytics without refactoring
- Independent scaling of analytics and UI layers

Architecture diagrams are provided in:
- architecture.drawio
- architecture.png

---

## Analytics Explained

### Hedge Ratio (β)
Estimated using Ordinary Least Squares (OLS) regression and adapts dynamically to market conditions.

### Spread & Z-Score
The spread is constructed using the estimated hedge ratio, and the Z-score measures deviation from the rolling equilibrium.

### Stationarity (ADF Test)
The Augmented Dickey-Fuller test validates mean-reverting behavior before signal interpretation.

### Rolling Correlation
Measures relationship stability between paired assets and acts as a risk filter.

### Mean-Reversion Half-Life
Estimates the expected time for the spread to revert toward its mean, helping assess signal timing.

### Mini Mean-Reversion Backtest
A lightweight rule-based simulation:
- Entry: |Z| > threshold
- Exit: |Z| < 0.5  
Used for intuition and validation, not performance claims.

---

## Trader Interpretation Layer

The dashboard includes a trader-oriented interpretation panel that combines:
- Z-score magnitude
- Stationarity confirmation
- Correlation stability
- Mean-reversion half-life

This layer bridges raw statistical outputs and practical trading intuition.

---

## Alerts

Context-aware alerts are triggered when Z-score thresholds are breached.  
Each alert includes supporting metrics to reduce false positives and provide situational awareness.

---

## Technology Stack

- Language: Python 3.x
- Data Ingestion: Binance WebSocket API
- Database: SQLite
- Analytics: pandas, numpy, statsmodels
- Visualization / UI: Streamlit, Plotly

---

## Project Structure

Gems_cap/
│
├── app.py
├── ingestion/
│ └── binance_ws.py
├── storage/
│ └── db.py
├── analytics/
│ ├── resampling.py
│ ├── regression.py
│ ├── spread.py
│ ├── correlation.py
│ ├── stationarity.py
│ ├── halflife.py
│ └── backtest.py
├── architecture.drawio
├── architecture.png
└── market_data.db
---

## How to Run

1. **Install dependencies**

   ```bash
   pip install streamlit pandas numpy statsmodels websocket-client
   ```

2. **Navigate to the project root**

   ```bash
   cd Gems_cap
   ```

3. **Run the application**

   ```bash
   python -m streamlit run app.py
   ```

This single command launches the **complete ingestion, analytics, alerting, and visualization pipeline** locally.

4. Open the browser at:

   ```
   http://localhost:8501
   ```

---

## Interpretation of Outputs

* **Hedge Ratio (β):**
  Estimated via rolling-window OLS regression and varies dynamically with market conditions.

* **Z-Score:**
  Measures deviation of the spread from its rolling mean. Alerts are triggered only when deviations are statistically significant.

* **Rolling Correlation:**
  Computed over short rolling windows and expected to fluctuate at high-frequency resolutions.

* **Price Chart:**
  BTC and ETH prices are plotted on the same axis, resulting in scale dominance by BTC. This behavior is intentional and reflects raw price dynamics.

These characteristics are **expected and realistic**, particularly at second-level granularity.

---

## Design Decisions & Trade-offs

* Streamlit was chosen to prioritize analytical clarity and rapid prototyping over UI complexity.
* A rolling visualization window is used to maintain responsiveness under continuous real-time updates.
* Full tick-level data is persisted to allow reproducibility and offline analysis.
* Analytics computations are cached where appropriate to balance computational cost and real-time behavior.
* Ingestion, analytics, storage, and visualization layers are isolated to support extensibility and future scaling.

---

## ChatGPT Usage Transparency

ChatGPT was used as a development aid for:

* Structuring the system architecture and module boundaries
* Debugging Python, WebSocket, and Streamlit integration issues
* Clarifying statistical methods such as OLS regression and stationarity testing

All core logic, architectural decisions, and final implementation choices were reviewed and validated manually.

---

## Notes

* This project is intended as a **quantitative analytics demonstration**, not a production trading system.
* The focus is on correctness, transparency, and explainability rather than signal optimization or execution.

---

## Author

**Tanushree Prakash Kanade**
