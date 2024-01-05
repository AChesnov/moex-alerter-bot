import logging
import os
import sys

CHAT_ID = "-4156438666"
WEBHOOK_PATH = "/"
WEBHOOK_URL = f"https://rnymo-81-222-178-138.a.free.pinggy.online{WEBHOOK_PATH}"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
LOGGER = logging.getLogger("moex_bot_alerter")
