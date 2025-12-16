import pandas as pd
from typing import List, Tuple


def ticks_to_dataframe(rows: List[Tuple]) -> pd.DataFrame:
   
    df = pd.DataFrame(
        rows,
        columns=["timestamp", "price", "quantity"]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="ISO8601",
        errors="coerce"
    )

    df.dropna(subset=["timestamp"], inplace=True)

    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)

    return df


def resample_ticks(
    df: pd.DataFrame,
    timeframe: str
) -> pd.DataFrame:
    
    rule_map = {
        "1s": "1S",
        "1m": "1T",
        "5m": "5T"
    }

    if timeframe not in rule_map:
        raise ValueError("Invalid timeframe")

    resampled = df.resample(rule_map[timeframe]).agg({
        "price": "last",
        "quantity": "sum"
    })

    resampled.dropna(inplace=True)

    return resampled
