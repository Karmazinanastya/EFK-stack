from telegram import Update
from telegram.ext import Application, CommandHandler
import logging
from datetime import datetime
import socket
import json

# Налаштування стандартного логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція надсилання логів у Logstash через TCP
def send_log_to_logstash(data: dict):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("logstash", 5000))  # 'logstash' — ім'я сервісу з docker-compose
        s.send((json.dumps(data) + "\n").encode("utf-8"))
        s.close()
    except Exception as e:
        logger.error(f"Error sending log to logstash: {e}")

# Обробник /start
async def start(update: Update, context):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Привіт! Поточний час: {current_time}")

    # Надсилаємо лог в Logstash
    send_log_to_logstash({
        "user": update.effective_user.username,
        "chat_id": update.effective_chat.id,
        "command": "/start",
        "timestamp": current_time
    })

# Обробка помилок
def error(update: Update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Запуск
def main():
    application = Application.builder().token("8075517888:AAG6a1zUnd0BOoEaSkWbbh5f2Xin40BQfGY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
