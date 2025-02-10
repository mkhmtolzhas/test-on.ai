from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from src.database import Base
from datetime import datetime


idpk = Annotated[int, mapped_column(primary_key=True, index=True)]
CreatedAt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE(('utc'), now())"))]
UpdatedAt = Annotated[datetime, mapped_column(server_default=text("TIMEZONE(('utc'), now())"), onupdate=datetime.utcnow)]


class MessageModel(Base):
    __tablename__ = "messages"

    id: idpk
    text: str
    created_at: CreatedAt
    updated_at: UpdatedAt