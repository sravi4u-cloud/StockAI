import requests

# Replace with your Telegram Bot Token and Chat ID
BOT_TOKEN = "8727403962:AAGtnz2WJyuj1WPAaABD5RB_knUpjh9Fl3g"
CHAT_ID = "1920028587"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print("Failed to send Telegram alert.")

    except Exception as e:
        print(f"Error sending Telegram alert: {e}")