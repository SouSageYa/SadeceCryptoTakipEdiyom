import ccxt
import pandas as pd
import time

# Binance API'ye bağlan
binance = ccxt.binance()

def get_market_data(symbol, timeframe='5m', limit=100):
    """
    Binance API'den belirli bir kripto paranın OHLCV verilerini çeker.
    :param symbol: Örneğin 'BTC/USDT'
    :param timeframe: Zaman dilimi ('1m', '5m', '1h', '1d' gibi)
    :param limit: Kaç mum çekeceğimiz
    :return: Pandas DataFrame formatında OHLCV verisi
    """
    try:
        data = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None

if __name__ == "__main__":
    # BTC/USDT için 5 dakikalık mumları çekelim
    btc_data = get_market_data('BTC/USDT')
    print(btc_data.tail())  # Son 5 satırı göster
