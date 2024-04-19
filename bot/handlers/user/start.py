from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from database.commands.user import get_user_by_tg_id
from database.commands.tg_spam import get_tg_user, add_tg_user

from keyboards.inline.user.main_keyboards import get_main_keyboard

from utils.texts.texts import main_text

router: Router = Router()


@router.message(CommandStart())
async def start_bot(message: Message, session: AsyncSession) -> None:
    await message.answer(main_text, reply_markup=await get_main_keyboard())
    response_win = await get_user_by_tg_id(session=session, tg_id=message.from_user.id)
    response_tg = await get_tg_user(session=session, tg_id=message.from_user.id)
    if response_win or response_tg:
        return
    await add_tg_user(session=session, tg_id=message.from_user.id, first_name=message.from_user.first_name)


@router.callback_query(F.data == 'back_button')
async def close_message_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(main_text, reply_markup=await get_main_keyboard())
    await state.clear()
