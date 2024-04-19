from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.commands.tg_spam import get_count_tg_spam
from database.commands.user import (
    get_count_user_in_deposit,
    get_count_user_in_vip_access,
    get_count_user_reg_in_one_win,
    get_count_user_reg_tg_one_wim
)

from utils.states.admin import Admin

from keyboards.inline.admin.admin_panel import get_button_back_admin_panel


router: Router = Router()


@router.callback_query(Admin.admin_panel, F.data == 'get_stats_bot')
async def get_stats_bot(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.set_state(Admin.get_stats)
    user_deposit = await get_count_user_in_deposit(session)
    user_in_vip = await get_count_user_in_vip_access(session)
    user_one_win = await get_count_user_reg_in_one_win(session)
    user_reg = await get_count_user_reg_tg_one_wim(session)
    user_tg = await get_count_tg_spam(session)

    await callback.message.edit_text(
        text="Пользователи: \n\n"
             f"👤 Зарегестрированные на one win и в боте: {user_reg}\n"
             f"👟 Зарегестрированные на one win: {user_one_win}\n"
             f"💸 Внесшие депозит: {user_deposit}\n"
             f"👑 Получившие доступ к вип: {user_in_vip}\n"
             f"✈️ Зафиксированные в боте, но нету аккаунта на one win: {user_tg}",
        reply_markup=get_button_back_admin_panel()
    )


