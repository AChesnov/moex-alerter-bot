from aiogram.fsm.state import State, StatesGroup


class AddTickerForm(StatesGroup):
    NAME = State()
    SHORT_NAME = State()
