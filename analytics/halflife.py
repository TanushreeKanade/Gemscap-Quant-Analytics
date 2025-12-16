import numpy as np
import statsmodels.api as sm

def compute_half_life(spread):
    spread_lag = spread.shift(1).dropna()
    spread_ret = spread.diff().dropna()

    spread_lag = spread_lag.loc[spread_ret.index]
    spread_lag_const = sm.add_constant(spread_lag)

    model = sm.OLS(spread_ret, spread_lag_const).fit()
    beta = model.params[1]

    if beta >= 0:
        return None

    half_life = -np.log(2) / beta
    return round(half_life, 2)
