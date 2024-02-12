from aiogram.utils.keyboard import InlineKeyboardBuilder

from moex_alerter_bot.keyboards.callback_data import (
    MenuAction,
    MenuActionType,
    StockAnalyzeAction,
    StockAnalyzeActionType,
    StockSelected,
)
from moex_alerter_bot.models.stock import Stock


def get_menu_keyboard():
    """Выводит основную клавиатуру с настройками"""
    keyword_builder = InlineKeyboardBuilder()
    keyword_builder.button(
        text='Add stock',
        callback_data=MenuAction(action=MenuActionType.ADD),
    )
    keyword_builder.button(
        text='Select stock',
        callback_data=MenuAction(action=MenuActionType.SELECT),
    )
    keyword_builder.button(
        text='Delete all stock monitoring',
        callback_data=MenuAction(action=MenuActionType.DELETE),
    )
    keyword_builder.adjust(1, 1)
    return keyword_builder.as_markup()


def get_stock_selector_keyboard(stocks: list[Stock]):
    """Выводит клавиатуру для выбора акции, по которой нужна настройка"""
    keyword_builder = InlineKeyboardBuilder()
    for stock in stocks:
        keyword_builder.button(text=stock.name, callback_data=StockSelected(name=stock.name))
    keyword_builder.adjust(5)
    return keyword_builder.as_markup()


def get_stock_menu(stock_id: int):
    """Выводит клавиатуру с настройками для акций"""
    keyword_builder = InlineKeyboardBuilder()
    keyword_builder.button(
        text='Add monitoring levels',
        callback_data=StockAnalyzeAction(action=StockAnalyzeActionType.ADD, stock_id=stock_id),
    )
    keyword_builder.button(
        text='Delete monitoring levels',
        callback_data=StockAnalyzeAction(action=StockAnalyzeActionType.DELETE, stock_id=stock_id),
    )
    keyword_builder.button(
        text='Show current monitoring settings',
        callback_data=StockAnalyzeAction(action=StockAnalyzeActionType.SHOW, stock_id=stock_id),
    )
    keyword_builder.adjust(1, 1)
    return keyword_builder.as_markup()
