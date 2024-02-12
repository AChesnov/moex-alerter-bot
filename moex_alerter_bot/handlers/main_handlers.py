from aiogram import Bot, types

from moex_alerter_bot.keyboards.inline import get_menu_keyboard


async def start(message: types.Message, bot: Bot):
    await message.answer('Hi')


async def stop(message: types.Message, bot: Bot):
    await message.answer('By')


async def settings(message: types.Message, bot: Bot):
    await message.answer(text='Menu:', reply_markup=get_menu_keyboard())
