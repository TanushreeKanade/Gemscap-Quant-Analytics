import pandas as pd
from statsmodels.tsa.stattools import adfuller


def adf_test(series: pd.Series) -> dict:
   
    series = series.dropna()

    result = adfuller(series)

    output = {
        "adf_statistic": result[0],
        "p_value": result[1],
        "critical_values": result[4]
    }

    return output
