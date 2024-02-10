from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError
from utils.states import AddTickerForm

from moex_alerter_bot.core import db
from moex_alerter_bot.keyboards.callback_data import MenuAction
from moex_alerter_bot.keyboards.inline import (
    get_menu_keyboard,
    get_stock_selector_keyboard,
)
from moex_alerter_bot.models.stock import Stock


async def start(message: types.Message):
    await message.answer('Hi')


async def stop(message: types.Message, bot: Bot):
    await message.answer('By')


async def settings(message: types.Message):
    await message.answer(text='Menu:', reply_markup=get_menu_keyboard())


async def got_ticker_name(message: types.Message, state: FSMContext):
    if True:
        # TODO: Тут будет проверка на наличие в БД и наличия на moex и вернем ошибку
        pass
    await message.answer(text='Enter ticker short_name')
    await state.update_data(name=message.text)
    await state.set_state(AddTickerForm.SHORT_NAME)


async def got_ticker_short_name(message: types.Message, state: FSMContext):
    await state.update_data(short_name=message.text)
    context_data = await state.get_data()
    await state.clear()

    try:
        stock = Stock(name=context_data['name'], short_name=context_data['short_name'])
        await db.add_stock(stock=stock)
    except IntegrityError:
        await message.answer(text='Stock already exist')
    else:
        await message.answer(text=f'Successful added: {stock!s}')


async def callback_setting(call: types.CallbackQuery, bot: Bot, callback_data: MenuAction, state: FSMContext):
    if callback_data.action == 'select_stock':
        stocks = await db.get_stocks()
        await call.message.answer(text='Available stocks:', reply_markup=get_stock_selector_keyboard(stocks))
    if callback_data.action == 'add_stock':
        await call.message.answer(text='Enter ticker name:')
        await state.set_state(AddTickerForm.NAME)
    if callback_data.action == 'delete_setting':
        await call.message.answer('Enter in delete_setting')
    await call.answer()
