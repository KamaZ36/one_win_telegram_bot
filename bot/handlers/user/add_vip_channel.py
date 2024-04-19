from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.callback_query import CallbackQuery

from database.commands.user import get_user_by_tg_id, get_user_by_win_id, update_tg_id_by_win_id, update_access_vip
from database.commands.tg_spam import delete_tg_user

from utils.states.userst import UserSt

from keyboards.inline.user.close_message import get_back_button

from settings import settings


router: Router = Router()


@router.callback_query(F.data == 'add_vip_access')
async def get_vip_channel_dostup(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    response = await get_user_by_tg_id(session=session, tg_id=callback.from_user.id)
    if response:
        if response.vip_access:
            await callback.message.edit_text("Вы уже получали доступ в вип-канал!", reply_markup=await get_back_button())
            return
        if not response.deposit:
            await callback.message.edit_text(
                "Для получения доступа в вип-канал, вам нужно внести депозит на сайте 1 WIN"
                "Внесите депозит, затем повторно нажмите кнопку.",
                reply_markup=await get_back_button()
            )
            return
        link = await bot.create_chat_invite_link(chat_id=settings.id_private_channel, member_limit=1)
        await callback.message.answer(
            f"Регистрация прошла успешно✅\n\n"
            f"Ссылка на VIP канал: {link.invite_link}\n\n"
            f"‼️ <b>Внимание</b> ‼️\nТолько 1 вступление по ссылке!"
        )
        await update_access_vip(session=session, tg_id=callback.from_user.id)
        return
    await state.set_state(UserSt.waiting_win_id)
    await callback.message.edit_text("Введите свой ID аккаунта на 1 WIN: ", reply_markup=await get_back_button())


@router.message(UserSt.waiting_win_id, F.text)
async def get_win_id_user(message: Message, state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    if not message.text.isdigit():
        await message.answer("Некорректно указан ID", reply_markup=await get_back_button())
        return
    response = await get_user_by_win_id(session=session, win_id=int(message.text))
    if not response:
        await message.answer("Ваш ID сайта 1 WIN не найден в базе данных!", reply_markup=await get_back_button())
        return
    await delete_tg_user(session=session, tg_id=message.from_user.id)
    await update_tg_id_by_win_id(
        session=session,
        tg_id=message.from_user.id,
        win_id=int(message.text),
        tg_name=message.from_user.first_name
    )
    user = await get_user_by_tg_id(session=session, tg_id=message.from_user.id)
    if not user.deposit:
        await message.answer(
            "Для получения доступа в VIP канал, вам нужно внести депозит на 1 WIN",
            reply_markup=await get_back_button()
        )
        return
    await update_access_vip(session=session, tg_id=message.from_user.id)
    await state.clear()
    link = await bot.create_chat_invite_link(chat_id=settings.id_private_channel, member_limit=1)
    await message.answer(
        f"Регистрация прошла успешно✅\n\n"
        f"Ссылка на VIP канал: {link.invite_link}\n\n"
        f"‼️ <b>Внимание</b> ‼️\nТолько 1 вступление по ссылке!"
    )

