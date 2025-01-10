from typing import Any

from sqlalchemy import BIGINT, VARCHAR, JSON
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class UserStateOrm(Base):
    __tablename__ = 'user_state'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    thread_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True)
    business_connection_id: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)
    destiny: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    state: Mapped[str | None] = mapped_column(VARCHAR, default=None, nullable=True)
