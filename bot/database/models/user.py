from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    win_id: Mapped[int] = mapped_column(BigInteger(), unique=True, nullable=True, default=None)
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, nullable=True, default=None)
    deposit: Mapped[bool] = mapped_column(default=False, nullable=True)
    vip_access: Mapped[bool] = mapped_column(default=False, nullable=True)
    tg_name: Mapped[str] = mapped_column(nullable=True, default='None')
