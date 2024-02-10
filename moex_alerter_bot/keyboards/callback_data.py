from aiogram.filters.callback_data import CallbackData


class MenuAction(CallbackData, prefix='menu_action'):
    action: str


class StockAction(CallbackData, prefix='stock_action'):
    action: str
