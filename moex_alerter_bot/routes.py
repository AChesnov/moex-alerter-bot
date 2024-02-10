from aiogram import Dispatcher, filters

from moex_alerter_bot import handlers
from moex_alerter_bot.keyboards.callback_data import MenuAction
from moex_alerter_bot.utils.states import AddTickerForm


def register_routes(dispatcher: Dispatcher):
    dispatcher.message.register(handlers.start, filters.command.Command('start'))
    dispatcher.message.register(handlers.stop, filters.command.Command('stop'))

    dispatcher.message.register(handlers.settings, filters.command.Command('settings'))
    dispatcher.callback_query.register(handlers.callback_setting, MenuAction.filter())

    dispatcher.message.register(handlers.got_ticker_name, AddTickerForm.NAME)
    dispatcher.message.register(handlers.got_ticker_short_name, AddTickerForm.SHORT_NAME)
