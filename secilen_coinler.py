import json
from coin_secimi import find_best_coins

def save_selected_coins():
    """
    Seçilen coinleri JSON dosyasına kaydeder.
    """
    selected_coins = find_best_coins()

    with open("secilen_coinler.json", "w") as f:
        json.dump(selected_coins, f, indent=4)

    print("\n📌 Seçilen coinler kaydedildi: secilen_coinler.json")

def load_selected_coins():
    """
    JSON dosyasından seçilen coinleri yükler.
    """
    try:
        with open("secilen_coinler.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

if __name__ == "__main__":
    save_selected_coins()
    print(f"\n📌 Yüklenen coinler: {load_selected_coins()}")
