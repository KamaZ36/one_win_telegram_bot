from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Статистика', callback_data='get_stats_bot')],
        [InlineKeyboardButton(text='Сделать рассылку', callback_data='start_spam_in_user')],
        [InlineKeyboardButton(text='Выйти', callback_data='close_admin_panel')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_back_admin_panel() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Назад', callback_data='back_in_admin_panel')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

