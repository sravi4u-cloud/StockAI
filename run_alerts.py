import sys
import os

# Add StockAI project folder to Python path

sys.path.append("/Users/ravisrivastava/StockAI")

from watchlist.alerts import get_price_alerts
from watchlist.telegram_alert import send_telegram_message

alerts = get_price_alerts()

for alert in alerts:
 if alert["alert"] == "BUY NOW":
  message = (
f"🚨 BUY NOW ALERT 🚨\n\n"
f"Stock: {alert['symbol']}\n"
f"Live Price: ₹{alert['live_price']}\n"
f"Target Price: ₹{alert['target_price']}\n\n"
f"StockAI has detected a buying opportunity."
)

send_telegram_message(message)

print("Alert check completed successfully.")
