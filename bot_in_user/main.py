import asyncio

from pyrogram import Client, filters, idle
from pyrogram.types import Message

from database.engine import create_database_pool

from config import config

from database.commands.user import (
    get_user_by_win_id,
    create_user,
    update_deposit_by_win_id
)

app = Client(
        name=config.session_name,
        api_hash=config.api_hash,
        api_id=config.api_id,
    )


db_pool = create_database_pool(config.create_dsn_postgresql(), logging=False)


async def read_chat_add_users() -> None:
    """Проверка наличия новых пользователей при первом запуске программы и добавление их в базу данных"""

    print("Выполнение скрипта по добавлению старых юзеров")
    messages = app.get_chat_history(chat_id=config.chat_one_win)
    i = 0
    add_mess = 0
    edit_dep = 0

    async for message in messages:
        i += 1
        print(f"Читаем сообщение {i}")
        try:
            if "депозит" in message.text:
                win_id = int(message.text.split(':')[0])
                async with db_pool.begin() as session:
                    response = await get_user_by_win_id(session=session, win_id=win_id)
                if not response:
                    async with db_pool.begin() as session:
                        await create_user(session=session, win_id=win_id, deposit=True)
                async with db_pool.begin() as session:
                    await update_deposit_by_win_id(session=session, win_id=win_id)
                edit_dep += 1

            elif message.text.isdigit():
                async with db_pool.begin() as session:
                    response = await get_user_by_win_id(session=session, win_id=int(message.text))
                if not response:
                    async with db_pool.begin() as session:
                        await create_user(session=session, win_id=int(message.text), deposit=False)
                    add_mess += 1
                else:
                    continue
        except AttributeError as ex:
            pass
        except ValueError:
            pass
        except TypeError:
            pass
    print(f"Прочитано: {i} сообщений")
    print(f"Добавлено в бд: {add_mess} юзеров.")
    print(f"Внесли депозит: {edit_dep} юзеров.")


@app.on_message(filters.chat(config.chat_one_win) & filters.text)
async def start(client: Client, message: Message) -> None:
    """Отслеживание чата с 1 win"""

    if 'депозит' in message.text:
        win_id = int(message.text.split(':')[0])
        async with db_pool.begin() as session:
            response = await get_user_by_win_id(session=session, win_id=win_id)
            if not response:
                await create_user(session=session, win_id=int(message.text), deposit=True)
                return
            await update_deposit_by_win_id(session=session, win_id=win_id)
    elif message.text.isdigit():
        async with db_pool.begin() as session:
            response = await get_user_by_win_id(session=session, win_id=int(message.text))
            if response:
                return
            await create_user(session=session, win_id=int(message.text), deposit=False)


async def main() -> None:
    await app.start()
    await read_chat_add_users()
    print("Бот запущен")
    await idle()


if __name__ == '__main__':
    print("Запуск бота")
    app.run(main())
