from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard():
    keyword_builder = InlineKeyboardBuilder()
    keyword_builder.button(text="1", callback_data="1")
    keyword_builder.button(text="2", callback_data="2")
    keyword_builder.button(text="3", callback_data="3")
    keyword_builder.button(text="4", callback_data="4")
    keyword_builder.button(text="5", callback_data="5")
    keyword_builder.button(text="6", callback_data="6")
    keyword_builder.adjust(3, 3)
    return keyword_builder.as_markup()
