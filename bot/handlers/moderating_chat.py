from aiogram import Router, F
from aiogram.types import Message
from filters.chat_type import ChatTypeFilter

router: Router = Router()


@router.message(ChatTypeFilter(chat_type=['supergroup']))
async def moderating_chat(message: Message):
    print("Апдейт в чате модерации!")
    if message.photo:
        await message.delete()
    elif 'https://' in message.text:
        await message.delete()
    elif message.text:
        with open('stop-words.txt', 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
            for word in words:
                if word.lower() in message.text.lower():
                    print(f'{word.lower()} {message.text.lower()}')
                    await message.delete()


