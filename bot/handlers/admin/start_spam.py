import asyncio
from typing import Any

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from utils.states.admin import Admin

from database.commands.tg_spam import get_all_tg_user

from keyboards.inline.admin.admin_panel import get_button_back_admin_panel, get_admin_panel_keyboard
from keyboards.inline.admin.spam_keyboard import get_spam_keyboard


router: Router = Router()


async def delete_media_group(bot: Bot, chat_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    if not data['media_id']:
        return
    for media_id in data['media_id']:
        await bot.delete_message(chat_id, media_id)
    await state.update_data(media_id=[])


async def create_media_group(data: dict[str, Any], caption: str = None) -> MediaGroupBuilder | bool:
    if caption is None:
        media_group = MediaGroupBuilder()
    else:
        media_group = MediaGroupBuilder(caption=caption)

    if data['photos'] or data['videos']:
        for photo in data['photos']:
            media_group.add_photo(media=photo)
        for video in data['videos']:
            media_group.add_video(media=video)
    else:
        return False

    return media_group


@router.callback_query(Admin.admin_panel, F.data == 'start_spam_in_user')
async def start_spam_in_user(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.waiting_spam_text)
    await state.update_data(photos=[], videos=[], media_id=[])
    call = await callback.message.edit_text(
        "Введите текст, который вы хотите отправить всем: ",
        reply_markup=get_button_back_admin_panel()
    )
    await state.update_data(msg_id=call.message_id)


@router.message(Admin.waiting_spam_text, F.text)
async def get_text_in_spam(message: Message, state: FSMContext, bot: Bot) -> None:
    """Получение текста для поста спама"""

    data = await state.get_data()
    await state.set_state(Admin.spam_menu)
    await state.update_data(text=message.text)
    await bot.delete_message(chat_id=message.chat.id, message_id=data['msg_id'])
    await message.delete()
    await message.answer(message.text, reply_markup=await get_spam_keyboard())


@router.callback_query(Admin.spam_menu, F.data == 'edit_text_spam')
async def edit_text_spam(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Редактирование текста поста спама"""

    await state.set_state(Admin.waiting_spam_text)
    button = [[InlineKeyboardButton(text='Отмена', callback_data='cancel_edit_text_in_spam')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    call = await callback.message.edit_text(
        "Введите текст, который вы хотите отправить всем: ",
        reply_markup=keyboard
    )
    data = await state.get_data()
    if 'media_id' in data:
        await delete_media_group(bot=bot, chat_id=callback.message.chat.id, state=state)
    await state.update_data(msg_id=call.message_id)


@router.callback_query(Admin.waiting_spam_text, F.data == 'cancel_edit_text_in_spam')
async def cancel_edit_text(callback: CallbackQuery, state: FSMContext) -> None:
    """Выход из редактирования текста обратно в спам-меню"""

    data = await state.get_data()
    await state.set_state(Admin.spam_menu)
    await callback.message.edit_text(data['text'], reply_markup=await get_spam_keyboard())


@router.callback_query(Admin.spam_menu, F.data == 'add_photo_spam')
async def add_photo_spam(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Добавление фото для поста спама"""

    await state.set_state(Admin.waiting_spam_photo)
    button = [[InlineKeyboardButton(text='Отмена', callback_data='cancel_add_photo_in_spam')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await delete_media_group(bot=bot, chat_id=callback.message.chat.id, state=state)
    call = await callback.message.edit_text("Отправьте фото, которое хотите прикрепить: ", reply_markup=keyboard)
    await state.update_data(msg_id=call.message_id)


@router.callback_query(StateFilter(Admin.waiting_spam_photo, Admin.waiting_spam_video)  , F.data == 'cancel_add_photo_in_spam')
async def cancel_add_photo_in_spam(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Выход из добавления фото для поста спама обратно в меню спама"""

    await state.set_state(Admin.spam_menu)
    data = await state.get_data()
    await callback.message.edit_text(data['text'], reply_markup=await get_spam_keyboard())


@router.message(Admin.waiting_spam_photo, F.photo)
async def get_photo_in_spam(message: Message, state: FSMContext, bot: Bot) -> None:
    """Ждем фото и добавляем его ид в список фотографий"""

    data = await state.get_data()
    data['photos'].append(message.photo[-1].file_id)
    await state.update_data(photos=data['photos'])
    await state.set_state(Admin.spam_menu)

    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data['msg_id'])
    await message.answer("Фотография добавлена.", reply_markup=await get_spam_keyboard())


@router.callback_query(Admin.spam_menu, F.data == 'add_video_spam')
async def add_video_spam(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Добавление видео для поста спама"""

    await state.set_state(Admin.waiting_spam_video)
    button = [[InlineKeyboardButton(text='Отмена', callback_data='cancel_add_photo_in_spam')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await delete_media_group(bot=bot, chat_id=callback.message.chat.id, state=state)
    call = await callback.message.edit_text("Отправьте видео, которое хотите прикрепить: ", reply_markup=keyboard)
    await state.update_data(msg_id=call.message_id)


@router.message(Admin.waiting_spam_video, F.video)
async def get_video_spam(message: Message, state: FSMContext, bot: Bot) -> None:
    """Получение видео и добавление его ид в список видео"""

    data = await state.get_data()
    data['videos'].append(message.video.file_id)
    await state.update_data(viedos=data['videos'])
    await state.set_state(Admin.spam_menu)

    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data['msg_id'])
    await message.answer("Видео добавлено.'", reply_markup=await get_spam_keyboard())


@router.callback_query(Admin.spam_menu, F.data == 'show_spam_post_end')
async def show_spam_post_end(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    await delete_media_group(state=state, bot=bot, chat_id=callback.message.chat.id)
    media_group = await create_media_group(data, caption=data['text'])
    await callback.message.delete()
    if media_group:
        msg = await callback.message.answer_media_group(media=media_group.build())
        for ms in msg:
            data['media_id'].append(ms.message_id)
        await state.update_data(media_id=data['media_id'])
    else:
        msg = await callback.message.answer(data['text'])
        await state.update_data(media_id=[msg.message_id])
    await callback.message.answer("Меню: ", reply_markup=await get_spam_keyboard())


@router.callback_query(Admin.spam_menu, F.data == 'start_spam')
async def start_spam(callback: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession) -> None:
    await delete_media_group(state=state, bot=bot, chat_id=callback.message.chat.id)

    await callback.message.edit_text("Начинаем рассылку..")
    data = await state.get_data()
    task = asyncio.create_task(start_spam_posts(session=session, data=data, bot=bot, callback=callback))
    await callback.message.edit_text(f"Идет рассылка... Отправлено: 0 сообщений.")
    messages_send = await task
    await callback.message.edit_text(f"Рассылка завершена.\n\nПолучилось отправить: {messages_send} сообщений.", reply_markup=get_admin_panel_keyboard())
    await state.set_data({})
    await state.set_state(Admin.admin_panel)


async def start_spam_posts(session: AsyncSession, data: dict[str, Any], bot: Bot, callback: CallbackQuery) -> int:
    """Алгоритм рассылки"""

    i: int = 0
    send_messages: int = 0
    try:
        users = await get_all_tg_user(session)
        if not data['photos'] and not data['videos']:
            for user in users:
                if i == 20:
                    await asyncio.sleep(1)
                    i = 0
                    await callback.message.edit_text(f'Идет рассылка... Отправлено: {send_messages} сообщений.')
                try:
                    await bot.send_message(chat_id=user.tg_id, text=data['text'])
                except Exception:
                    pass
                i += 1
                send_messages += 1
            return send_messages

        media_group = await create_media_group(data, caption=data['text'])
        for user in users:
            if i == 20:
                await asyncio.sleep(1)
                i = 0
                await callback.message.edit_text(f'Идет рассылка... Отправлено: {send_messages} сообщений.')
            try:
                await bot.send_media_group(chat_id=user.tg_id, media=media_group.build())
            except Exception:
                pass
            i += 1
            send_messages += 1
        return send_messages
    except asyncio.CancelledError:
        return send_messages
