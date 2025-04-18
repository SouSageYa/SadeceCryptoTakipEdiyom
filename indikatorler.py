import pandas as pd
import ta  # Teknik analiz için kütüphane

def calculate_indicators(df):
    """
    Verilen OHLCV verisinden teknik indikatörleri hesaplar.
    :param df: Pandas DataFrame (OHLCV formatında olmalı)
    :return: Güncellenmiş DataFrame
    """

    # EMA (Exponential Moving Average) hesapla
    df['EMA_20'] = ta.trend.ema_indicator(df['close'], window=20)
    df['EMA_50'] = ta.trend.ema_indicator(df['close'], window=50)

    # MACD hesapla
    df['MACD'] = ta.trend.macd(df['close'])
    df['MACD_Signal'] = ta.trend.macd_signal(df['close'])

    # RSI (Relative Strength Index) hesapla
    df['RSI'] = ta.momentum.rsi(df['close'])

    # Bollinger Bands hesapla
    bb = ta.volatility.BollingerBands(df['close'], window=20)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()

    # VWAP (Volume Weighted Average Price)
    df['VWAP'] = ta.volume.volume_weighted_average_price(df['high'], df['low'], df['close'], df['volume'])

    # OBV (On-Balance Volume) hesapla
    df['OBV'] = ta.volume.on_balance_volume(df['close'], df['volume'])

    # ATR (Average True Range) hesapla
    df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)

    # Donchian Channel hesapla
    df['Donchian_Upper'] = df['high'].rolling(window=20).max()  # Üst seviye
    df['Donchian_Lower'] = df['low'].rolling(window=20).min()   # Alt seviye

    # Fibonacci Retracement hesapla (Son 10 mumun en yüksek ve en düşük fiyatlarına göre)
    df['Fib_High'] = df['high'].rolling(window=10).max()
    df['Fib_Low'] = df['low'].rolling(window=10).min()
    df['Fibonacci'] = df['Fib_Low'] + (df['Fib_High'] - df['Fib_Low']) * 0.618  # %61.8 seviyesi

    return df
