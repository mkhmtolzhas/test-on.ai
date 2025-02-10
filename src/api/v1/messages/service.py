from .model import MessageModel
from .schemas import MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession


class MessageService:
    @staticmethod
    async def create_message(session: AsyncSession, message: MessageSchema):
        message = MessageModel(**message.model_dump())
        session.add(message)
        await session.commit()
        return message
    
    