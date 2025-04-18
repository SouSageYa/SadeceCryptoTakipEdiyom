import ccxt
import pandas as pd
from indikatorler import calculate_indicators  # İndikatörleri hesaplamak için


def get_recent_data(symbol="BTC/USDT", timeframe="5m", limit=100):
    """
    Binance API'den belirtilen coinin son 'limit' adetlik tarihsel verisini çeker.

    :param symbol: İşlem çifti (ör: "BTC/USDT")
    :param timeframe: Zaman aralığı (ör: "5m", "1h", "1d")
    :param limit: Çekilecek veri sayısı (ör: 100)
    :return: Pandas DataFrame olarak mum verileri
    """
    binance = ccxt.binance()

    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)

        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df

    except Exception as e:
        print(f"⚠️ Binance API Hatası: {e}")
        return None


def analyze_data(df):
    """
    İlk 60 barı analiz eder ve sinyal oluşturur.
    :param df: Pandas DataFrame (100 satırlık veri)
    :return: Sinyal (BUY / HOLD / SELL), giriş fiyatı
    """
    df = calculate_indicators(df)  # İndikatörleri hesapla

    last_analysed_bar = df.iloc[59]  # 60. barı analiz noktası olarak al
    entry_price = last_analysed_bar["close"]

    # **BUY Sinyali Koşulları**
    buy_signal = 0
    if last_analysed_bar["EMA_20"] > last_analysed_bar["EMA_50"]: buy_signal += 1
    if last_analysed_bar["MACD"] > last_analysed_bar["MACD_Signal"]: buy_signal += 1
    if last_analysed_bar["RSI"] > 50: buy_signal += 1
    if last_analysed_bar["BB_High"] > last_analysed_bar["close"]: buy_signal += 1
    if last_analysed_bar["BB_Low"] < last_analysed_bar["close"]: buy_signal += 1
    if last_analysed_bar["VWAP"] < last_analysed_bar["close"]: buy_signal += 1
    if last_analysed_bar["OBV"] > df["OBV"].iloc[58]: buy_signal += 1
    if last_analysed_bar["Fibonacci"] < last_analysed_bar["close"]: buy_signal += 1
    if last_analysed_bar["Donchian_Upper"] < last_analysed_bar["close"]: buy_signal += 1
    if last_analysed_bar["ATR"] < df["ATR"].mean(): buy_signal += 1

    # Sinyal karar mekanizması
    if buy_signal >= 6:
        return "BUY", entry_price
    elif buy_signal <= 3:
        return "SELL", entry_price
    else:
        return "HOLD", entry_price


def backtest(symbol="BTC/USDT"):
    """
    Backtest fonksiyonu:
    - 100 bar verisi alır.
    - İlk 60 barda analiz yaparak sinyal oluşturur.
    - Kalan 40 barda sinyalin doğruluğunu test eder.
    """

    df = get_recent_data(symbol, "5m", 100)
    if df is None or len(df) < 100:
        print(f"⚠️ {symbol} için yeterli veri bulunamadı!")
        return

    # Sinyal oluştur
    signal, entry_price = analyze_data(df)

    # 40 bar sonrası en yüksek fiyatı kontrol et
    future_prices = df.iloc[60:]["close"]  # Son 400 bar
    exit_price = future_prices.max()  # En yüksek fiyat

    # Sonuç hesaplama
    if signal == "BUY":
        result = "✅ Doğru" if exit_price > entry_price else "❌ Yanlış"
    else:
        result = "⏳ Test edilmedi"

    # Sonuçları göster
    results = pd.DataFrame([{
        "symbol": symbol,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "signal": signal,
        "result": result
    }])

    print("\n📊 Backtest Sonucu:")
    print(results)


# **Örnek kullanım:**
if __name__ == "__main__":
    backtest("ETH/USDT")  # BTC/USDT için backtest yap
