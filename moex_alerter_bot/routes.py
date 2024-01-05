from moex_alerter_bot import handlers
from moex_alerter_bot.config import DP

from aiogram import filters


def register_routes():
    DP.message.register(handlers.start, filters.command.Command("start"))
    DP.message.register(handlers.stop, filters.command.Command("stop"))
    DP.message.register(handlers.settings, filters.command.Command("settings"))
