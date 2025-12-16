import pandas as pd
import statsmodels.api as sm


def align_pairs(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
   
    aligned = df_a[["price"]].join(
        df_b[["price"]],
        how="inner",
        lsuffix="_a",
        rsuffix="_b"
    )

    return aligned


def compute_hedge_ratio(aligned_df: pd.DataFrame):
   
    y = aligned_df["price_a"]
    x = aligned_df["price_b"]

    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()

    beta = model.params["price_b"]
    alpha = model.params["const"]

    return beta, alpha
