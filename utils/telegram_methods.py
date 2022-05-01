import telegram
from utils import common_methods
import time

bot = telegram.Bot(token=common_methods.TELEGRAM_TOKEN)


def send_to_telegram(message, group_id=common_methods.TELEGRAM_METRICS_GROUP_ID) -> Boolean:
    """
    "message" is sent to a Telegram group using a Telegram Bot.
    Args:
        message: Message to send
        group_id: Telegram group ID to send the message to
    Returns:
        Boolean: True if message was sent successfully, False otherwise
    """
    max_retries = 3
    retries = 0
    print(message)
    while retries < max_retries:
        try:
            bot.send_message(text=message, chat_id=group_id)
            return True
        except telegram.error.TimedOut as timeout:
            time.sleep(1*retries)
            print("Retrying...")
            retries += 1
        except telegram.error.RetryAfter as retry_after:
            return False # Usually it requests as to wait 40 seconds before retrying. As it's being persisted in cloudwatch, we can pass.


def send_exception_to_telegram(message, exception):
    """
    A message and an exception are sent to a Telegram group using a Telegram Bot.
    Exception traceback is also being printed on screen (sent to Cloudwatch) for debugging purposes.
    Args:
        message: Custom message to send
        exception: Exception to send
    Returns:
        Boolean: True if message was sent successfully, False otherwise
    """
    message_to_send = f"{message}. \n " \
                      f"Exception type: {type(exception)}. \n" \
                      f"Exception message: {exception}. \n"
    send_to_telegram(message=message_to_send)
    print(f"Exception traceback: {traceback.format_exc()}")


def send_document_to_telegram(file_path, file_name):
    """
    A document is sent to a Telegram group using a Telegram Bot.
    Args:
        file_path: Path to the file to send
        file_name: Name of the file to send
    Returns:
        Boolean: True if message was sent successfully, False otherwise
    """
    file = open(file_path, 'rb')
    bot.send_document(chat_id=common_methods.TELEGRAM_METRICS_GROUP_ID, document=file, filename=file_name)
    file.close()
