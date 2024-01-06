def is_doji(df):
    body_ = abs(df['Open'] - df['Close'])
    range_ = df['High'] - df['Low']
    return (body_ / range_) <= 0.1  # Adjust this threshold as needed

def is_bullish_engulfing(df):
    condition1 = df['Open'].shift(1) > df['Close'].shift(1)
    condition2 = df['Close'] > df['Open']
    condition3 = df['Close'] > df['Open'].shift(1)
    condition4 = df['Open'] < df['Close'].shift(1)
    return condition1 & condition2 & condition3 & condition4

def is_bearish_engulfing(df):
    condition1 = df['Open'].shift(1) < df['Close'].shift(1)
    condition2 = df['Close'] < df['Open']
    condition3 = df['Close'] < df['Close'].shift(1)
    condition4 = df['Open'] > df['Open'].shift(1)
    return condition1 & condition2 & condition3 & condition4
