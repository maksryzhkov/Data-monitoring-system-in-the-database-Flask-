import requests
import logging


def verify_and_init_bot(token: str, chat_id: str):
    """Автоматическая проверка и инициализация Telegram-бота при старте."""
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("Telegram Bot Token не задан. Включен режим консольных алертов (Mock mode).")
        return False

    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        res = requests.get(url, timeout=3).json()
        if res.get("ok"):
            bot_name = res["result"]["first_name"]
            bot_username = res["result"]["username"]
            print(f"Telegram-бот успешно подключен: @{bot_username} ({bot_name})")

            # Отправка приветственного анонса о запуске DQM
            if chat_id:
                send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": "🟢 <b>Data Quality Monitor запущен!</b>\nСистема готова к сканированию БД.",
                    "parse_mode": "HTML"
                }
                requests.post(send_url, json=payload, timeout=3)
            return True
        else:
            print(f"Ошибка токена Telegram: {res.get('description')}")
            return False
    except Exception as e:
        print(f"Не удалось связаться с Telegram API: {e}")
        return False