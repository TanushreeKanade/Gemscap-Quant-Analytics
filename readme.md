# Real-Time Pair Trading Analytics

**GemsCap – Quant Developer Evaluation (Round 1)**

---

## Overview

This project implements a **real-time quantitative analytics system for pair trading** using live Binance WebSocket market data. The application demonstrates an **end-to-end workflow** covering real-time data ingestion, persistent storage, time-series processing, statistical analytics, interactive visualization, and alerting, as required by the assignment.

The system is designed to emphasize **clean separation of concerns**, **statistical correctness**, and **realistic market behavior**, rather than synthetic or hardcoded outputs.

---

## Key Features

### Live Data Ingestion

* Real-time tick-level trade data streamed from the Binance WebSocket API for two symbols (BTCUSDT and ETHUSDT).
* Ingestion runs continuously and feeds downstream analytics without blocking the UI.

### Persistent Storage

* All incoming tick data is persisted in a local SQLite database to ensure durability, reproducibility, and offline analysis.

### Time-Series Processing

* Tick data is resampled into configurable timeframes:

  * 1 second
  * 1 minute
  * 5 minutes

### Pair Trading Analytics

* OLS-based hedge ratio (β) estimation
* Spread computation between paired assets
* Z-score of the spread using rolling statistics
* Rolling correlation
* Augmented Dickey-Fuller (ADF) test for stationarity

### Interactive Dashboard (Streamlit)

* Near real-time analytics updates
* Adjustable rolling window size
* User-defined Z-score alert thresholds
* CSV export of processed analytics
* Interactive charts supporting zoom, pan, and hover

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

The architecture is intentionally **modular and loosely coupled**, allowing:

* Easy integration of additional data sources (REST APIs, historical CSV uploads)
* Extension with new analytics modules without impacting existing components
* Future scaling to higher-frequency data or alternative markets without frontend changes

---

## Technology Stack

* **Language:** Python 3.x
* **Data Ingestion:** Binance WebSocket API
* **Database:** SQLite
* **Analytics:** pandas, numpy, statsmodels
* **Visualization / UI:** Streamlit

---

## Project Structure

```
Gems_cap/
│
├── app.py                  # Streamlit UI & orchestration
│
├── ingestion/
│   ├── __init__.py
│   └── binance_ws.py       # WebSocket ingestion logic
│
├── storage/
│   ├── __init__.py
│   └── db.py               # SQLite schema & queries
│
├── analytics/
│   ├── __init__.py
│   ├── resampling.py       # Tick → bar conversion
│   ├── regression.py       # Pair alignment & OLS hedge ratio
│   ├── spread.py           # Spread & Z-score
│   ├── correlation.py      # Rolling correlation
│   └── stationarity.py     # ADF test
│
└── market_data.db          # SQLite database (auto-created)
```

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
