from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery

from keyboards.inline.user.close_message import get_back_button

from utils.texts.texts import register_one_win

router: Router = Router()


@router.callback_query(F.data == '1win_register')
async def get_register_links(callback: CallbackQuery) -> None:
    await callback.message.edit_text(register_one_win, reply_markup=await get_back_button())
