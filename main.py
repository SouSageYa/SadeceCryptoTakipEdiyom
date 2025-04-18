import time
from secilen_coinler import save_selected_coins
from coin_takip import track_selected_coins
from telegram_bildirim import send_signal_notifications

def main():
    """
    Tüm sistemi otomatik çalıştıran ana fonksiyon.
    """
    while True:
        print("\n🚀 **Yeni Döngü Başlıyor...**\n")

        # 1️⃣ En iyi coinleri seç ve kaydet
        print("📌 Coin seçimi yapılıyor...")
        save_selected_coins()

        # 2️⃣ Seçilen coinleri takip et ve sinyalleri hesapla
        print("📊 Coin trendleri takip ediliyor...")
        track_selected_coins()

        # 3️⃣ Sinyalleri Telegram'a gönder
        print("📢 Telegram'a sinyaller gönderiliyor...")
        send_signal_notifications()

        # 4️⃣ 10 dakika bekle ve döngüyü tekrar et
        print("\n⏳ 1 Saat bekleniyor...\n")
        time.sleep(30)  # 1 Saat

if __name__ == "__main__":
    main()
