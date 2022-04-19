import telegram
from utils import common_methods
import time

bot = telegram.Bot(token=common_methods.TELEGRAM_TOKEN)

def send_to_telegram(message, group_id=common_methods.TELEGRAM_METRICS_GROUP_ID):
    """
    "message" is sent to a Telegram group using a Telegram Bot.
    Args:
        message: Message to send
    Returns:
        None
    """
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            bot.send_message(text=message, chat_id=group_id)
        except telegram.error.TimedOut as timeout:
            time.sleep(1*retries)
            print("Retrying...")
            retries += 1


def send_document_to_telegram(file_path, file_name):
    file = open(file_path, 'rb')
    bot.send_document(chat_id=common_methods.TELEGRAM_METRICS_GROUP_ID, document=file, filename=file_name)
    file.close()
