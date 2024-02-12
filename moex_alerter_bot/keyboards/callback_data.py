from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MenuActionType(Enum):
    SELECT = 'select_stock'
    ADD = 'add_stock'
    DELETE = 'delete_setting'


class StockAnalyzeActionType(Enum):
    ADD = 'add'
    DELETE = 'delete'
    SHOW = 'show'


class MenuAction(CallbackData, prefix='menu_action'):
    action: MenuActionType


class StockSelected(CallbackData, prefix='stock_selected'):
    name: str


class StockAnalyzeAction(CallbackData, prefix='stock_analyze_action'):
    action: StockAnalyzeActionType
    stock_id: int
