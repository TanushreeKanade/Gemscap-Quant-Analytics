import pandas as pd

def simple_mean_reversion_backtest(spread, zscore, entry=2.0, exit=0.5):
    position = 0
    pnl = []

    for i in range(1, len(spread)):
        z = zscore.iloc[i]

        if position == 0:
            if z > entry:
                position = -1
            elif z < -entry:
                position = 1

        elif position != 0 and abs(z) < exit:
            position = 0

        pnl.append(position * (spread.iloc[i] - spread.iloc[i-1]))

    return pd.DataFrame({
        "Spread": spread.iloc[1:].values,
        "Z-Score": zscore.iloc[1:].values,
        "PnL": pnl
    })
