import logging
import os
from aiogram import Dispatcher, Bot

MOEX_URL = "https://iss.moex.com/iss"
TG_URL = "https://api.telegram.org/bot"
CHAT_ID = "-4156438666"
HTML_FORMAT = "html"
MARKDOWN_FORMAT = "MarkdownV2"
WEBHOOK_PATH = "/"
WEBHOOK_URL = f"https://rnwzz-81-222-178-138.a.free.pinggy.online{WEBHOOK_PATH}"

LOGGER = logging.getLogger("uvicorn")
BOT = Bot(token=os.getenv("BOT_TOKEN", ""))
DP = Dispatcher()
