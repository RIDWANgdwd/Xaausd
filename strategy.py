"""
Logic strategi: EMA Trend Filter + Asia Session Breakout + ATR untuk SL/TP.
Butuh: pip install pandas numpy
"""
import pandas as pd
import numpy as np

from config import (
    EMA_FAST, EMA_SLOW, ATR_PERIOD,
    ATR_SL_MULTIPLIER, ATR_TP_MULTIPLIER,
    ASIA_SESSION_START_HOUR_WIB, ASIA_SESSION_END_HOUR_WIB,
)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Tambah kolom EMA fast/slow dan ATR ke DataFrame candle."""
    df = df.copy()
    df["ema_fast"] = df["close"].ewm(span=EMA_FAST, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=EMA_SLOW, adjust=False).mean()

    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = true_range.rolling(ATR_PERIOD).mean()

    return df


