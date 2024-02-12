from aiogram import Dispatcher, filters

from moex_alerter_bot.handlers import main_handlers, stock_analyze_handlers, stock_handlers
from moex_alerter_bot.keyboards.callback_data import MenuAction, StockAnalyzeAction, StockSelected
from moex_alerter_bot.utils.states import AddStockAnalyzeForm, AddStockForm


def register_routes(dispatcher: Dispatcher):
    dispatcher.message.register(main_handlers.start, filters.command.Command('start'))
    dispatcher.message.register(main_handlers.stop, filters.command.Command('stop'))
    dispatcher.message.register(main_handlers.settings, filters.command.Command('settings'))

    dispatcher.callback_query.register(stock_handlers.callback_setting, MenuAction.filter())
    dispatcher.callback_query.register(stock_handlers.callback_stock_selected, StockSelected.filter())
    dispatcher.message.register(stock_handlers.got_ticker_name, AddStockForm.NAME)
    dispatcher.message.register(stock_handlers.got_ticker_short_name, AddStockForm.SHORT_NAME)

    dispatcher.callback_query.register(
        stock_analyze_handlers.callback_stock_analyze_selected,
        StockAnalyzeAction.filter(),
    )
    dispatcher.message.register(stock_analyze_handlers.got_stock_top_limit, AddStockAnalyzeForm.TOP_LIMIT)
    dispatcher.message.register(stock_analyze_handlers.got_stock_bottom_limit, AddStockAnalyzeForm.BOTTOM_LIMIT)
