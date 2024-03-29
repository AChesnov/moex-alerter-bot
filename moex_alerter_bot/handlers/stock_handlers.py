from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from moex_alerter_bot.core import db
from moex_alerter_bot.core.moex_api_client import MoexApiClient
from moex_alerter_bot.keyboards.callback_data import MenuAction, MenuActionType, StockSelected
from moex_alerter_bot.keyboards.inline import get_stock_menu, get_stock_selector_keyboard
from moex_alerter_bot.models.stock import Stock
from moex_alerter_bot.utils.states import AddStockForm


async def got_ticker_name(message: types.Message, state: FSMContext):
    """Когда получили ticker_name, проверяем что такой есть api_moex и сохраняем в БД"""
    await state.update_data(name=message.text.upper())
    context_data = await state.get_data()
    await state.clear()

    moex_api = MoexApiClient()
    stock_info = await moex_api.get_stock_info(stock_name=context_data['name'])
    if not stock_info:
        await message.answer(text='Stock not found via moex_api')
        return

    try:
        stock = Stock(name=stock_info.name, short_name=stock_info.short_name)
        await db.add_object(object_type=stock)
    except IntegrityError:
        await message.answer(text='Stock already exist')
    else:
        await message.answer(text=f'Successfully added: {stock!s}')


async def callback_setting(call: types.CallbackQuery, bot: Bot, callback_data: MenuAction, state: FSMContext):
    await state.clear()
    match callback_data.action:
        case MenuActionType.SELECT:
            stocks = await db.get_stocks()
            await call.message.answer(text='Available stocks:', reply_markup=get_stock_selector_keyboard(stocks))
        case MenuActionType.ADD:
            await state.set_state(AddStockForm.NAME)
            await call.message.answer(text='Enter ticker name:')
        case MenuActionType.DELETE:
            await call.message.answer('Enter in delete_setting')

    await call.answer()


async def callback_stock_selected(call: types.CallbackQuery, bot: Bot, callback_data: StockSelected, state: FSMContext):
    stock = await db.get_stock(stock_name=callback_data.name)
    await call.message.answer(text='Stock monitoring settings:', reply_markup=get_stock_menu(stock_id=stock.id))
    await call.answer()
