import time
import json
from veri_cek import get_market_data
from indikatorler import calculate_indicators
from secilen_coinler import load_selected_coins
from telegram_bildirim import send_signal_notifications


def analyze_coin(symbol):
    """
    Seçilen coinin indikatörlerini hesaplayarak AL/SAT sinyali verir.
    """
    df = get_market_data(symbol)

    if df is None:
        print(f"⚠️ {symbol} için veri alınamadı!")
        return None

    df = calculate_indicators(df)
    latest = df.iloc[-1]  # Son satır (en güncel fiyat)

    buy_score = 0
    sell_score = 0

    # **ALIM SİNYALİ (BUY)**
    if latest["EMA_20"] > latest["EMA_50"]: buy_score += 1
    if latest["MACD"] > latest["MACD_Signal"]: buy_score += 1
    if latest["RSI"] > 50: buy_score += 1
    if latest["BB_High"] > latest["close"]: buy_score += 1
    if latest["VWAP"] < latest["close"]: buy_score += 1
    if latest["OBV"] > df["OBV"].iloc[-2]: buy_score += 1

    # **SATIŞ SİNYALİ (SELL)**
    if latest["EMA_20"] < latest["EMA_50"]: sell_score += 1
    if latest["MACD"] < latest["MACD_Signal"]: sell_score += 1
    if latest["RSI"] < 45: sell_score += 1

    signal = "HOLD"  # Varsayılan olarak bekle

    if buy_score >= 6:
        signal = "BUY"
    elif sell_score >= 3:
        signal = "SELL"

    return {
        "symbol": symbol,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "signal": signal
    }


def track_selected_coins():
    """
    Seçilen coinleri sürekli takip eder ve AL/SAT sinyali oluşturur.
    """
    while True:
        selected_coins = load_selected_coins()

        if not selected_coins:
            print("⚠️ Seçili coin bulunamadı! `secilen_coinler.py` dosyasını çalıştırarak coin seç.")
            return

        print("\n🔄 Coin takibi başlatıldı...")
        signals = []

        for coin in selected_coins:
            coin_symbol = coin[0]  # Örn: "BTC/USDT"
            result = analyze_coin(coin_symbol)
            if result:
                signals.append(result)

        # Sonuçları JSON olarak saklayalım
        with open("sinyaller.json", "w") as f:
            json.dump(signals, f, indent=4)

        print("\n📢 Güncellenmiş Sinyaller:")
        for s in signals:
            print(
                f"{s['symbol']} -> ALIM PUANI: {s['buy_score']}, SATIŞ PUANI: {s['sell_score']}, SİNYAL: {s['signal']}")

        print("\n⏳ 1 dakika bekleniyor...\n")
        time.sleep(60)  # 1 dakika bekle


if __name__ == "__main__":
    track_selected_coins()
    # Sinyaller güncellendikten sonra Telegram’a gönder
    send_signal_notifications()

