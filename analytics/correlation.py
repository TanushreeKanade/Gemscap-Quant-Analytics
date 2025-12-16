import pandas as pd


def compute_rolling_correlation(
    aligned_df: pd.DataFrame,
    window: int
) -> pd.Series:
    
    corr = (
        aligned_df["price_a"]
        .rolling(window)
        .corr(aligned_df["price_b"])
    )

    corr.name = "rolling_correlation"
    return corr
