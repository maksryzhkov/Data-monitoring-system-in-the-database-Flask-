import os
from app.alerts import TelegramNotifier

# Вставь сюда реальные данные бота или передавай через environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

print("🧪 Тестирование отправки уведомлений в Telegram...")
notifier = TelegramNotifier(token=BOT_TOKEN, chat_id=CHAT_ID)

test_message = (
    "<b>DQM System Test Alert</b>\n\n"
    "Проверка интеграции с Telegram прошла успешно!\n"
    "Система готова к отправке аномалий."
)

success = notifier.send_alert(test_message)

if success:
    print("Сообщение успешно доставлено в Telegram!")
else:
    print("Сообщение выведено в консоль (заглушка/mock режим).")