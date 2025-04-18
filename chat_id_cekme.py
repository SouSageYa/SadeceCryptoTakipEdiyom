import requests

TOKEN = "7766842360:AAFdPkNQjak4D326HFpV2E31VjEWWoUONOI"  # BotFather'dan aldığın token
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(URL)
print(response.json())  # Burada "chat_id" değerini görebilirsin
