from aiogram.fsm.state import State, StatesGroup


class AddStockForm(StatesGroup):
    NAME = State()
    SHORT_NAME = State()


class AddStockAnalyzeForm(StatesGroup):
    STOCK_ID = State()
    TOP_LIMIT = State()
    BOTTOM_LIMIT = State()
