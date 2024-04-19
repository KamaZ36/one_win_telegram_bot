from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_back_button() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text='Назад', callback_data='back_button')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
