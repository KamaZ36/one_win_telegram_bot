from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    admin_panel: State = State()

    waiting_spam_text: State = State()
    spam_menu: State = State()
    waiting_spam_photo: State = State()
    waiting_spam_video: State = State()

    get_stats: State = State()


