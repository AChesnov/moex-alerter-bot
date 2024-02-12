from decimal import Decimal

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from moex_alerter_bot.core import db
from moex_alerter_bot.keyboards.callback_data import StockAnalyzeAction, StockAnalyzeActionType
from moex_alerter_bot.models.stock import StockAnalyze
from moex_alerter_bot.utils.states import AddStockAnalyzeForm


async def got_stock_top_limit(message: types.Message, state: FSMContext):
    """Когда получили top_limit для StockAnalyze, сохраняем его, меняем state и запрашиваем ввести bottom_limit"""
    await state.update_data(top_limit=Decimal(message.text))
    await state.set_state(AddStockAnalyzeForm.BOTTOM_LIMIT)
    await message.answer(text='Enter bottom limit')


async def got_stock_bottom_limit(message: types.Message, state: FSMContext):
    """Когда получили bottom_limit для StockAnalyze, сохраняем его, меняем state и сохраняем в БД"""
    await state.update_data(bottom_limit=Decimal(message.text))
    context_data = await state.get_data()
    await state.clear()

    try:
        stock_analyze = StockAnalyze(
            stock_id=context_data['stock_id'],
            top_limit=context_data['top_limit'],
            bottom_limit=context_data['bottom_limit'],
        )
        await db.add_object(object_type=stock_analyze)
    except IntegrityError:
        await message.answer(text='StockAnalyze already exist')
    else:
        await message.answer(text=f'Successfully added: {stock_analyze!s}')


async def callback_stock_analyze_selected(
    call: types.CallbackQuery,
    bot: Bot,
    callback_data: StockAnalyzeAction,
    state: FSMContext,
):
    await state.clear()
    match callback_data.action:
        case StockAnalyzeActionType.ADD:
            await state.set_state(AddStockAnalyzeForm.STOCK_ID)
            await state.update_data(stock_id=callback_data.stock_id)
            await state.set_state(AddStockAnalyzeForm.TOP_LIMIT)
            await call.message.answer(text='Enter top limit:')
        case StockAnalyzeActionType.DELETE:
            await db.delete_object(object_type=StockAnalyze, object_id=callback_data.stock_id)
        case StockAnalyzeActionType.SHOW:
            stock_analyze_data = await db.get_stock_analyze(stock_id=callback_data.stock_id)
            if stock_analyze_data:
                await call.message.answer(f'Current_setting: {stock_analyze_data}')
            else:
                await call.message.answer('Current setting is empty!')

    await call.answer()
