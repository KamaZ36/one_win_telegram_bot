from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_spam_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Изменить текст', callback_data='edit_text_spam')],
        [InlineKeyboardButton(text='Добавить фото', callback_data='add_photo_spam'),
         InlineKeyboardButton(text='Добавить видео', callback_data='add_video_spam')],
        [InlineKeyboardButton(text='Предпросмотр', callback_data='show_spam_post_end')],
        [InlineKeyboardButton(text='Начать рассылку', callback_data='start_spam')],
        [InlineKeyboardButton(text='Отмена', callback_data='back_in_admin_panel')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
