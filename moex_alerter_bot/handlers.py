from moex_alerter_bot.config import LOGGER
from moex_alerter_bot.keyboards.inline import get_inline_keyboard

from aiogram import types, Bot


async def start(message: types.Message):
    await message.answer("Hi")


async def stop(message: types.Message, bot: Bot):
    await message.answer("By")


async def settings(message: types.Message):
    LOGGER.info("settings")
    await message.answer(text="Ok", reply_markup=get_inline_keyboard())
