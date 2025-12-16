import pandas as pd


def compute_spread(
    aligned_df: pd.DataFrame,
    hedge_ratio: float
) -> pd.Series:
   
    spread = aligned_df["price_a"] - hedge_ratio * aligned_df["price_b"]
    spread.name = "spread"
    return spread


def compute_zscore(
    spread: pd.Series,
    window: int
) -> pd.Series:
   
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()

    zscore = (spread - rolling_mean) / rolling_std
    zscore.name = "zscore"

    return zscore
