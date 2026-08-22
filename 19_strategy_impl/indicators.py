"""Self-contained technical indicators (no pandas_ta dependency).

Only needs pandas + numpy. Column names and values match pandas_ta 0.4.x
(the direction column is bit-identical; the bands agree to ~1e-14), so this
is a drop-in replacement:

    import indicators as ta
    sup = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    df['supertrend'] = sup['SUPERTd_10_3.0']
    df['ema'] = ta.ema(df['close'], length=10)
"""

import numpy as np
import pandas as pd


def true_range(high, low, close):
    """True Range: max(high-low, |high-prev_close|, |prev_close-low|).

    The first bar has no previous close, so it is NaN (same as TA-Lib).
    """
    pc = close.shift(1)
    tr = pd.concat([high - low, (high - pc).abs(), (pc - low).abs()], axis=1).max(axis=1)
    tr.iloc[0] = np.nan
    tr.name = "TRUERANGE_1"
    return tr


def rma(close, length=10):
    """Wilder's Moving Average: an EMA with alpha = 1 / length."""
    out = close.ewm(alpha=1.0 / length, adjust=False).mean()
    out.name = f"RMA_{length}"
    return out


def sma(close, length=10):
    out = close.rolling(length).mean()
    out.name = f"SMA_{length}"
    return out


def ema(close, length=10, presma=True):
    """Exponential Moving Average, seeded with an SMA like TA-Lib."""
    close = close.astype(float).copy()
    if presma:
        sma_nth = close.iloc[0:length].mean()
        close.iloc[: length - 1] = np.nan
        close.iloc[length - 1] = sma_nth
    out = close.ewm(span=length, adjust=False).mean()
    out.name = f"EMA_{length}"
    return out


def atr(high, low, close, length=14, mamode="rma", percent=False):
    """Average True Range (Wilder), matching TA-Lib.

    The first ``length`` values are NaN; index ``length`` is seeded with the
    simple average of true ranges 1..length, and every bar after that is
    smoothed recursively: atr = (prev_atr * (length - 1) + tr) / length.
    """
    tr = true_range(high, low, close)

    mamode = (mamode or "rma").lower()
    if mamode == "rma":
        seeded = tr.copy()
        seeded.iloc[:length] = np.nan
        seeded.iloc[length] = tr.iloc[1:length + 1].mean()
        out = rma(seeded, length=length)
    elif mamode == "ema":
        out = ema(tr, length=length)
    elif mamode == "sma":
        out = sma(tr, length=length)
    elif mamode == "wma":
        weights = np.arange(1, length + 1, dtype=float)
        out = tr.rolling(length).apply(
            lambda w: np.dot(w, weights) / weights.sum(), raw=True
        )
    else:
        raise ValueError(f"unsupported atr_mamode: {mamode!r}")

    if percent:
        out = out * (100 / close)

    out.name = f"ATR{mamode[0]}{'p' if percent else ''}_{length}"
    return out


def supertrend(high, low, close, length=7, atr_length=None, multiplier=3.0,
               atr_mamode="rma", offset=0):
    """Supertrend: trend direction plus trailing support/resistance bands.

    Returns a DataFrame with 4 columns, named exactly like pandas_ta:
        SUPERT_{length}_{multiplier}   trend line (long band or short band)
        SUPERTd_{length}_{multiplier}  direction:  1 = uptrend, -1 = downtrend
        SUPERTl_{length}_{multiplier}  the long band  (NaN while short)
        SUPERTs_{length}_{multiplier}  the short band (NaN while long)
    """
    if atr_length is None:
        atr_length = length

    high = pd.Series(high).astype(float)
    low = pd.Series(low).astype(float)
    close = pd.Series(close).astype(float)

    m = close.size
    if m < length + 1:
        return None

    dir_ = [1] * m
    trend = [0] * m
    long = [np.nan] * m
    short = [np.nan] * m

    hl2 = 0.5 * (high + low)
    matr = multiplier * atr(high, low, close, length=atr_length, mamode=atr_mamode)

    # mutable copies: the bands get clamped in place inside the loop
    lb = (hl2 - matr).to_numpy(dtype=float, copy=True)   # lower band
    ub = (hl2 + matr).to_numpy(dtype=float, copy=True)   # upper band
    c = close.to_numpy(dtype=float)

    for i in range(1, m):
        if c[i] > ub[i - 1]:
            dir_[i] = 1
        elif c[i] < lb[i - 1]:
            dir_[i] = -1
        else:
            dir_[i] = dir_[i - 1]
            # in an uptrend the lower band can only ratchet up, and vice versa
            if dir_[i] > 0 and lb[i] < lb[i - 1]:
                lb[i] = lb[i - 1]
            if dir_[i] < 0 and ub[i] > ub[i - 1]:
                ub[i] = ub[i - 1]

        if dir_[i] > 0:
            trend[i] = long[i] = lb[i]
        else:
            trend[i] = short[i] = ub[i]

    trend[0] = np.nan
    dir_[:length] = [np.nan] * length

    props = f"_{length}_{multiplier}"
    df = pd.DataFrame(
        {
            f"SUPERT{props}": trend,
            f"SUPERTd{props}": dir_,
            f"SUPERTl{props}": long,
            f"SUPERTs{props}": short,
        },
        index=close.index,
    )

    if offset != 0:
        df = df.shift(offset)

    return df


