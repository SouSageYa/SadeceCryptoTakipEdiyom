import ccxt
import pandas as pd


def get_recent_data(symbol="BTC/USDT", timeframe="5m", limit=100):
    """
    Binance API'den belirtilen coinin son 'limit' adetlik tarihsel verisini çeker.

    :param symbol: İşlem çifti (ör: "BTC/USDT")
    :param timeframe: Zaman aralığı (ör: "5m", "1h", "1d")
    :param limit: Çekilecek veri sayısı (ör: 100)
    :return: Pandas DataFrame olarak 5m mum verileri
    """
    binance = ccxt.binance()

    try:
        # Binance'ten mum verilerini çek
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)

        # Verileri DataFrame'e çevir
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # Timestamp'i okunabilir tarih formatına çevir
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df

    except Exception as e:
        print(f"⚠️ Binance API Hatası: {e}")
        return None


# Örnek kullanım: BTC/USDT için son 100 adet 5 dakikalık veriyi çek
df = get_recent_data("BTC/USDT", "5m", 100)

# Veriyi ekrana yazdır
if df is not None:
    import ace_tools as tools

    tools.display_dataframe_to_user(name="Son 100 adet 5 dakikalık BTC/USDT verisi", dataframe=df)
