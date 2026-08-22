import requests

def verify_and_init_bot(token: str, chat_id: str):
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("Telegram Bot Token не задан. Включен Mock mode.")
        return False

    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("ok"):
            bot_name = res["result"]["first_name"]
            bot_username = res["result"]["username"]
            print(f"Telegram-бот успешно подключен: @{bot_username} ({bot_name})")
            return True
        else:
            print(f"Ошибка токена Telegram: {res.get('description')}")
            return False
    except Exception as e:
        print(f"Ошибка сети при запросе к Telegram API: {e}")
        return False