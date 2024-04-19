from aiogram.fsm.state import State, StatesGroup


class UserSt(StatesGroup):
    waiting_win_id: State = State()

