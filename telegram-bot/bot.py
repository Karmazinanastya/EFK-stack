from telegram import Update
from telegram.ext import Application, CommandHandler
import logging
from datetime import datetime
import socket
import json

from prometheus_client import start_http_server, Counter, Summary

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

START_COMMAND_COUNT = Counter("start_command_total", "Total number of /start command calls")
RESPONSE_TIME = Summary("response_time_seconds", "Time spent processing /start command")

def send_log_to_logstash(data: dict):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("logstash", 5000)) 
        s.send((json.dumps(data) + "\n").encode("utf-8"))
        s.close()
    except Exception as e:
        logger.error(f"Error sending log to logstash: {e}")

@RESPONSE_TIME.time()
async def start(update: Update, context):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Привіт! Поточний час: {current_time}")

    START_COMMAND_COUNT.inc()

    send_log_to_logstash({
        "user": update.effective_user.username,
        "chat_id": update.effective_chat.id,
        "command": "/start",
        "timestamp": current_time
    })

def error(update: Update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    start_http_server(9091)

    application = Application.builder().token("8075517888:AAG6a1zUnd0BOoEaSkWbbh5f2Xin40BQfGY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
