import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def get_handler():
    if log_file := os.getenv('LOG_FILE'):
        return logging.FileHandler(log_file, encoding='utf-8')  # Пишем в файл
    return logging.StreamHandler(stream=sys.stdout)  # Пишем в stdout


def get_logger():
    # Будут строки вида: "[2017-08-23 09:54:55,356] [moex_bot_alerter] main.py:34 [DEBUG] foo"
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(filename)s:%(lineno)d [%(levelname)s] %(message)s')

    handler = get_handler()
    handler.setFormatter(formatter)

    for logger_name in ('root', 'moex_bot_alerter'):
        log = logging.getLogger(logger_name)
        log.setLevel(logging.DEBUG)
        log.propagate = False
        log.addHandler(handler)

    return logging.getLogger('moex_bot_alerter')


BOT_TOKEN = str(os.getenv('BOT_TOKEN', ''))
CHAT_ID = str(os.getenv('CHAT_ID', ''))
WEBHOOK_PATH = str(os.getenv('WEBHOOK_PATH', '/'))
WEB_SERVER_HOST = str(os.getenv('WEB_SERVER_HOST', '0.0.0.0'))
WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT', 8081))
WEBHOOK_URL = str(os.getenv('WEBHOOK_URL', ''))
DB_URL = str(os.getenv('DB_URL', ''))
LOGGER = get_logger()
