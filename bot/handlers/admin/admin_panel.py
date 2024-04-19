from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery

from utils.states.admin import Admin

from filters.check_user_in_admin import IsUserInAdmin

from handlers.admin.start_spam import delete_media_group

from keyboards.inline.admin.admin_panel import get_admin_panel_keyboard

router: Router = Router()


@router.message(Command('admin'), IsUserInAdmin())
async def get_admin_panel(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    if 'media_id' in data:
        await delete_media_group(chat_id=message.chat.id, state=state, bot=bot)
    await state.set_data({})
    await state.set_state(Admin.admin_panel)
    await message.delete()
    await message.answer("Админ-панель: ", reply_markup=get_admin_panel_keyboard())


@router.callback_query(F.data == 'back_in_admin_panel')
async def back_in_admin_panel(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    if 'media_id' in data:
        await delete_media_group(chat_id=callback.message.chat.id, state=state, bot=bot)
    await state.set_data({})
    await state.set_state(Admin.admin_panel)
    await callback.message.edit_text("Админ-панель: ", reply_markup=get_admin_panel_keyboard())


@router.callback_query(F.data == 'close_admin_panel')
async def close_admin_panel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
