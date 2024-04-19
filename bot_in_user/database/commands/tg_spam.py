from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.tg_spam import TgSpam


async def add_tg_user(session: AsyncSession, tg_id: int, first_name: str) -> None:
    user = TgSpam(
        tg_id=tg_id,
        first_name=first_name,
    )
    session.add(user)
    await session.commit()


async def get_tg_user(session: AsyncSession, tg_id: int) -> TgSpam | bool:
    query = select(TgSpam).where(TgSpam.tg_id == tg_id)
    response = await session.execute(query)
    if not response:
        return False
    user = response.scalar()
    return user


async def delete_tg_user(session: AsyncSession, tg_id: int) -> None:
    query = delete(TgSpam).where(TgSpam.tg_id == tg_id)
    await session.execute(query)
    await session.commit()


async def get_all_tg_user(session: AsyncSession) -> Sequence[TgSpam] | bool:
    query = select(TgSpam)
    response = await session.execute(query)
    if not response:
        return False
    tg_spams = response.scalars().all()
    return tg_spams
