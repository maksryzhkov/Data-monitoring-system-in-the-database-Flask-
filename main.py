import os
from app import create_app
from app.bot_setup import verify_and_init_bot
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Авто-проверка и инициализация бота при запуске сервера
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    verify_and_init_bot(bot_token, chat_id)

    app.run(debug=True, port=5000)
