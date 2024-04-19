from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='🚀 Регистрация на 1 WIN', callback_data='1win_register')],
        [InlineKeyboardButton(text='👑 Получить доступ к VIP', callback_data='add_vip_access')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
