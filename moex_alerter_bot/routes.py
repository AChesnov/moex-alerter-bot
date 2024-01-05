from moex_alerter_bot import handlers

from aiogram import filters
from aiogram import Dispatcher


def register_routes(dispatcher: Dispatcher):
    dispatcher.message.register(handlers.start, filters.command.Command("start"))
    dispatcher.message.register(handlers.stop, filters.command.Command("stop"))
    dispatcher.message.register(handlers.settings, filters.command.Command("settings"))
