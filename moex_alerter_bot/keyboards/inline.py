from aiogram.utils.keyboard import InlineKeyboardBuilder

from moex_alerter_bot.core.moex_api_client import Stock
from moex_alerter_bot.keyboards.callback_data import MenuAction


def get_menu_keyboard():
    keyword_builder = InlineKeyboardBuilder()
    keyword_builder.button(text='Add stock', callback_data=MenuAction(action='add_stock'))
    keyword_builder.button(text='Select stock', callback_data=MenuAction(action='select_stock'))
    keyword_builder.button(
        text='Delete all stock monitoring',
        callback_data=MenuAction(action='delete_setting'),
    )
    keyword_builder.adjust(1, 1)
    return keyword_builder.as_markup()


def get_stock_selector_keyboard(stocks: list[Stock]):
    keyword_builder = InlineKeyboardBuilder()

    for ticker in stocks:
        keyword_builder.button(text=ticker.name, callback_data=ticker.name)
    keyword_builder.adjust(5)
    return keyword_builder.as_markup()
