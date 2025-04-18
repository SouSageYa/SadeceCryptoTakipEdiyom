import requests
import json

# 📌 BURAYA KENDİ TELEGRAM TOKEN'İNİ VE CHAT ID'İNİ GİR
TELEGRAM_BOT_TOKEN = "7766842360:AAFdPkNQjak4D326HFpV2E31VjEWWoUONOI"
TELEGRAM_CHAT_ID = "6548010572"


def send_telegram_message(message):
    """
    Telegram botu ile belirlenen chat ID'ye mesaj gönderir.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Telegram'a mesaj gönderildi!")
    else:
        print(f"❌ Telegram gönderim hatası: {response.text}")


def send_signal_notifications():
    """
    Sinyalleri okur ve Telegram'a gönderir.
    """
    try:
        with open("sinyaller.json", "r") as f:
            signals = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Sinyal dosyası bulunamadı!")
        return

    if not signals:
        print("⚠️ Gönderilecek sinyal yok!")
        return

    for signal in signals:
        message = f"📢 *Kripto Sinyali*\n\n" \
                  f"🪙 *Coin:* {signal['symbol']}\n" \
                  f"📊 *ALIM PUANI:* {signal['buy_score']}\n" \
                  f"📉 *SATIŞ PUANI:* {signal['sell_score']}\n" \
                  f"📌 *Sinyal:* {signal['signal']}\n"

        send_telegram_message(message)


if __name__ == "__main__":
    send_signal_notifications()
