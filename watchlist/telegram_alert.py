import requests

BOT_TOKEN = "8727403962:AAGtnz2WJyuj1WPAaABD5RB_knUpjh9Fl3g"
CHAT_ID = "1920028587"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    return response.json()


if __name__ == "__main__":
    # Test message
    send_telegram_message("StockAI Telegram notification is working! 🚀")

