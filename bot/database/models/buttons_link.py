from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ButtonsLink(Base):
    __tablename__ = 'buttons_link'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
