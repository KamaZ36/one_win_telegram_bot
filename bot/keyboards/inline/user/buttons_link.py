from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.commands.buttons_link import get_buttons_link
from database.models.buttons_link import ButtonsLink


async def get_link_buttons(session: AsyncSession) -> InlineKeyboardMarkup:
    buttons = []
    links: Sequence[ButtonsLink] = await get_buttons_link(session)
    for link in links:
        buttons.append([InlineKeyboardButton(text=link.text, url=link.link)])
    buttons.append([InlineKeyboardButton(text='Скрыть', callback_data='close_message')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
