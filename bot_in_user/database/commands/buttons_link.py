from typing import Sequence

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.buttons_link import ButtonsLink


async def get_buttons_link(session: AsyncSession) -> Sequence[ButtonsLink] | bool:
    query = select(ButtonsLink)
    response = await session.execute(query)
    if not response:
        return False
    buttons_link = response.scalars().all()
    return buttons_link
