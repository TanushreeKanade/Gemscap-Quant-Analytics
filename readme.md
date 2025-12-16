# Real-Time Pair Trading Analytics (GemsCap – Round 1 Assignment)

## Overview
This project implements a **real-time quantitative analytics system for pair trading** using live Binance WebSocket market data. The system ingests tick-level trade data, stores it in a relational database, processes it into time-series bars, and computes core statistical metrics used in pair trading strategies. Results are visualized through an interactive Streamlit dashboard.

The design emphasizes **clean separation of concerns**, **statistical correctness**, and **realistic market behavior** rather than synthetic or hardcoded outputs.

---

## Key Features

- **Live Data Ingestion**  
  Real-time trade data streamed from Binance WebSocket API for two symbols (BTCUSDT and ETHUSDT).

- **Persistent Storage**  
  All ticks are stored in SQLite for durability and reproducibility.

- **Time-Series Processing**  
  Tick data is resampled into configurable timeframes (1s, 1m, 5m).

- **Pair Trading Analytics**  
  - OLS-based hedge ratio (β)
  - Spread computation
  - Z-score of spread
  - Rolling correlation
  - Augmented Dickey-Fuller (ADF) test for stationarity

- **Interactive Dashboard (Streamlit)**  
  - Real-time updates
  - Adjustable rolling window
  - Z-score alert thresholds
  - CSV export of analytics

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
```

---

## Technology Stack

- **Language:** Python 3.x
- **Data Ingestion:** Binance WebSocket API
- **Database:** SQLite
- **Analytics:** pandas, numpy, statsmodels
- **Visualization/UI:** Streamlit

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

2. **Navigate to project root**
   ```bash
   cd Gems_cap
   ```

3. **Run the application**
   ```bash
   python -m streamlit run app.py
   ```

4. Open the browser at:
   ```
   http://localhost:8501
   ```

---

## Interpretation of Outputs

- **Hedge Ratio (β):** Window-dependent OLS estimate; varies over time as market conditions change.
- **Z-Score:** Measures deviation of spread from its rolling mean. Alerts trigger only when statistically significant.
- **Rolling Correlation:** Computed on short rolling windows; expected to fluctuate at high-frequency resolutions.
- **Price Chart:** BTC and ETH are plotted on the same axis, leading to scale dominance by BTC. This reflects raw price behavior.

These behaviors are **intentional and realistic**, especially at second-level granularity.

---

## Design Decisions & Trade-offs

• Streamlit was chosen for rapid prototyping and clarity of analytics rather than UI perfection.
• A rolling visualization window is used to maintain dashboard responsiveness under continuous updates.
• Full historical tick-level data is persisted in SQLite for offline analysis and reproducibility.
• Analytics computations are cached to balance real-time behavior with computational efficiency.
• The system architecture is modular, allowing ingestion, storage, analytics, and visualization layers to evolve independently.


---

## Notes

- This project is intended as a **quant analytics demonstration**, not a production trading system.
- The focus is on correctness, transparency, and explainability rather than signal optimization.

---

## Author

Tanushree Prakash Kanade

