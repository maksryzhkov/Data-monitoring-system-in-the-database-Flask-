import os
import requests

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    def send_alert(self, message: str) -> bool:
        """Отправка алертов в Telegram."""
        if not self.token or not self.chat_id:
            print("[Mock Alert]: Telegram не настроен. Сообщение:")
            print(message)
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            data = response.json()
            if response.status_code == 200 and data.get("ok"):
                print("Уведомление успешно доставлено в Telegram!")
                return True
            else:
                print(f"Ошибка отправки Telegram: {data.get('description')}")
                return False
        except Exception as e:
            print(f"Ошибка соединения с Telegram API: {e}")
            return False