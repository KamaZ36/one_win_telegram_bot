from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User


async def create_user(session: AsyncSession, win_id: int = None, tg_id: int = None, deposit: bool = False) -> None:
    user = User(
        win_id=win_id,
        tg_id=tg_id,
        deposit=deposit,
    )
    session.add(user)
    await session.commit()


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | bool:
    query = select(User).where(User.tg_id == tg_id)
    response = await session.execute(query)
    if not response:
        return False
    user: User = response.scalar()
    return user


async def get_user_by_win_id(session: AsyncSession, win_id: int) -> User | bool:
    query = select(User).where(User.win_id == win_id)
    response = await session.execute(query)
    if not response:
        return False
    user: User = response.scalar()
    return user


async def update_tg_id_by_win_id(session: AsyncSession, tg_id: int, win_id: int, tg_name: str) -> None:
    query = update(User).where(User.win_id == win_id).values(tg_id=tg_id, tg_name=tg_name)
    await session.execute(query)
    await session.commit()


async def update_deposit_by_win_id(session: AsyncSession, win_id: int) -> None:
    """Фиксируем, что пользователь вносил депозит"""

    query = update(User).where(User.win_id == win_id).values(deposit=True)
    await session.execute(query)
    await session.commit()


async def update_access_vip(session: AsyncSession, tg_id: int) -> None:
    query = update(User).where(User.tg_id == tg_id).values(vip_access=True)
    await session.execute(query)
    await session.commit()
