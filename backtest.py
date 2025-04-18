import ccxt
import pandas as pd
import time
from veri_cek import get_market_data
from indikatorler import calculate_indicators

def analyze_buy_signal(df):
    """
    1000 barlık veri içinde herhangi bir noktada BUY sinyali oluşup oluşmadığını analiz eder.
    """
    df = calculate_indicators(df)  # İndikatörleri hesapla

    for i in range(len(df) - 1):
        buy_score = 0
        if df["EMA_20"].iloc[i] > df["EMA_50"].iloc[i]: buy_score += 1
        if df["MACD"].iloc[i] > df["MACD_Signal"].iloc[i]: buy_score += 1
        if df["RSI"].iloc[i] > 50: buy_score += 1
        if df["BB_High"].iloc[i] > df["close"].iloc[i]: buy_score += 1
        if df["BB_Low"].iloc[i] < df["close"].iloc[i]: buy_score += 1
        if df["VWAP"].iloc[i] < df["close"].iloc[i]: buy_score += 1
        if df["OBV"].iloc[i] > df["OBV"].iloc[i - 1]: buy_score += 1
        if df["Fibonacci"].iloc[i] < df["close"].iloc[i]: buy_score += 1
        if df["Donchian_Upper"].iloc[i] < df["close"].iloc[i]: buy_score += 1
        if df["ATR"].iloc[i] < df["ATR"].mean(): buy_score += 1

        if buy_score >= 6:
            return i, df["close"].iloc[i], buy_score  # BUY sinyali indexi, fiyatı ve puanı

    return None, None, None  # BUY sinyali oluşmadı

def analyze_sell_signal(df, buy_index):
    """
    BUY sinyalinden sonra SELL sinyali gelene kadar bekler.
    Eğer veriler biterse mevcut fiyattan çıkış yapar.
    """
    for i in range(buy_index + 1, len(df)):
        sell_score = 0
        if df["EMA_20"].iloc[i] < df["EMA_50"].iloc[i]: sell_score += 1
        if df["MACD"].iloc[i] < df["MACD_Signal"].iloc[i]: sell_score += 1
        if df["RSI"].iloc[i] < 50: sell_score += 1
        if df["BB_High"].iloc[i] < df["close"].iloc[i]: sell_score += 1
        if df["BB_Low"].iloc[i] > df["close"].iloc[i]: sell_score += 1
        if df["VWAP"].iloc[i] > df["close"].iloc[i]: sell_score += 1
        if df["OBV"].iloc[i] < df["OBV"].iloc[i - 1]: sell_score += 1
        if df["Fibonacci"].iloc[i] > df["close"].iloc[i]: sell_score += 1
        if df["Donchian_Lower"].iloc[i] > df["close"].iloc[i]: sell_score += 1

        if sell_score >= 6:
            return i, df["close"].iloc[i], sell_score  # SELL sinyali indexi, fiyatı ve puanı

    return None, df["close"].iloc[-1], None  # SELL sinyali bulunmazsa son fiyat üzerinden çıkış

def backtest():
    """
    Binance üzerindeki tüm işlem gören coinleri backtest eder.
    """
    binance = ccxt.binance()
    try:
        markets = binance.load_markets()
        usdt_pairs = [symbol for symbol in markets if symbol.endswith('/USDT')]

        results = []
        for coin in usdt_pairs:
            print(f"\n🔍 Backtest: {coin} için veri çekiliyor...")
            df = get_market_data(coin, limit=1000)  # 1000 veri çek

            if df is None or df.empty:
                print(f"⚠️ {coin} için yeterli veri bulunamadı!")
                continue

            buy_index, entry_price, buy_score = analyze_buy_signal(df)

            if buy_index is None:
                print(f"❌ {coin} için BUY sinyali bulunamadı.")
                continue

            sell_index, exit_price, sell_score = analyze_sell_signal(df, buy_index)

            if sell_index is None:
                sell_index = len(df) - 1  # Eğer SELL sinyali yoksa son barda çık
                sell_score = "Yok"

            profit = ((exit_price - entry_price) / entry_price) * 100  # Kar/zarar yüzdesi

            # Bilgileri ekrana yazdır
            print(f"✅ {coin} için BACKTEST SONUCU:")
            print(f"   - BUY Sinyali: {buy_index}. bar | Puan: {buy_score} | Fiyat: {entry_price}")
            print(f"   - SELL Sinyali: {sell_index}. bar | Puan: {sell_score} | Fiyat: {exit_price}")
            print(f"   - Bekleme Süresi: {sell_index - buy_index} bar")
            print(f"   - Kar/Zarar: {profit:.2f}%\n")

            results.append([coin, buy_index, buy_score, entry_price, sell_index, sell_score, exit_price, profit])

            time.sleep(2)  # **2 saniye bekleme süresi**

        # Sonuçları göster
        df_results = pd.DataFrame(results, columns=["symbol", "buy_index", "buy_score", "entry_price",
                                                    "sell_index", "sell_score", "exit_price", "profit_percent"])
        print("\n📊 Backtest Sonuçları:")
        print(df_results)

    except Exception as e:
        print(f"⚠️ Binance API Hatası: {e}")

if __name__ == "__main__":
    backtest()
