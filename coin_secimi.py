import ccxt
from veri_cek import get_market_data
from indikatorler import calculate_indicators

def get_binance_coins():
    """
    Binance API'den sadece 'TRADING' durumunda olan USDT paritesine sahip coinleri çeker.
    """
    binance = ccxt.binance()

    try:
        markets = binance.load_markets()
        usdt_pairs = [symbol for symbol, data in markets.items() if symbol.endswith('/USDT') and data['info']['status'] == 'TRADING']
        return usdt_pairs

    except Exception as e:
        print(f"Binance API Hatası: {e}")
        return []

def score_coin(symbol):
    """
    Belirli bir coinin son 50 barındaki indikatör skorunu hesaplar.
    """
    df = get_market_data(symbol, limit=200)

    if df is None or len(df) < 200:
        print(f"⚠️ {symbol}: Yeterli veri bulunamadı!")
        return 0  # Yeterli veri yoksa 0 puan ver

    df = calculate_indicators(df)
    last_50_bars = df.iloc[-200:]  # Son 50 barı analiz et

    total_score = 0
    for _, latest in last_50_bars.iterrows():
        score = 0
        # **Trend belirleme indikatörleri**
        if latest["EMA_20"] > latest["EMA_50"]: score += 1
        if latest["MACD"] > latest["MACD_Signal"]: score += 1
        if latest["RSI"] > 50: score += 1
        if latest["BB_High"] > latest["close"]: score += 1
        if latest["BB_Low"] < latest["close"]: score += 1

        # **Hacim ve likidite indikatörleri**
        if latest["VWAP"] < latest["close"]: score += 1
        if latest["OBV"] > df["OBV"].iloc[-2]: score += 1

        # **Destek ve direnç noktaları**
        if latest["Fibonacci"] < latest["close"]: score += 1
        if latest["Donchian_Upper"] < latest["close"]: score += 1

        # **Volatilite kontrolü**
        if latest["ATR"] < df["ATR"].mean(): score += 1

        total_score += score  # Tüm barlardaki skoru topluyoruz

    final_score = total_score / 200  # Ortalama skor hesaplanıyor
    print(f"📊 {symbol}: Ortalama Puan {final_score:.2f}")  # ✅ Hangi coin kaç puan almış görelim
    return final_score

def find_best_coins():
    """
    Binance'deki en yüksek skora sahip en iyi 2 coini seçer.
    """
    usdt_coins = get_binance_coins()
    scores = {}

    for coin in usdt_coins:
        print(f"🔍 Analiz ediliyor: {coin}")
        score = score_coin(coin)
        scores[coin] = score

    # Skorları sırala (en yüksek puandan en düşüğe)
    sorted_coins = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Eğer 6 puan üstü coin yoksa en azından en iyi 2 taneyi alalım
    best_coins = [coin for coin in sorted_coins if coin[1] >= 6]
    if len(best_coins) < 2:
        best_coins = sorted_coins[:2]  # En iyi 2 coini al (puan 6 olmasa bile)

    return best_coins

if __name__ == "__main__":
    best_coins = find_best_coins()
    print(f"\n📌 Seçilen 2 coin: {best_coins}")
