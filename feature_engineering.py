import pandas as pd

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret"] = out["close"].pct_change()
    out["volatility"] = out["ret"].rolling(20).std()
    return out
