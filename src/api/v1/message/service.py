from src.exeptions import GlobalException
from .model import MessageModel
from .schemas import MessageCreate, MessageInDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class MessageService:
    @staticmethod
    async def create_message(sesssion: AsyncSession, message: MessageCreate):
        try:
            new_message = MessageModel(**message.dict())
            sesssion.add(new_message)
            await sesssion.commit()
            await sesssion.refresh(new_message)

            new_message = MessageInDB().model_validate(new_message, from_attributes=True).model_dump()


            return {
                "message": "Message created successfully",
                "data": new_message
            }
        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))
        
    @staticmethod
    async def get_messages(session: AsyncSession, page: int = 1, limit: int = 10):
        try:
            stmt = select(MessageModel).order_by(MessageModel.created_at.desc()).limit(limit).offset((page - 1) * limit)
            result = await session.execute(stmt)
            messages = result.scalars().all()

            messages = MessageInDB().model_validate(messages, from_attributes=True).model_dump(many=True)

            return {
                "message": "Messages retrieved successfully",
                "data": messages
            }
        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))
        
    @staticmethod
    async def get_message(session: AsyncSession, message_id: int):
        try:
            stmt = select(MessageModel).where(MessageModel.id == message_id)
            result = await session.execute(stmt)
            message = result.scalars().first()

            if not message:
                raise GlobalException.NotFound(detail="Message not found")

            message = MessageInDB().model_validate(message, from_attributes=True).model_dump()

            return {
                "message": "Message retrieved successfully",
                "data": message
            }
        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))
        

    @staticmethod
    async def update_message(session: AsyncSession, message_id: int, message: MessageCreate):
        try:
            updated_message = session.get(MessageModel, message_id)
            if not updated_message:
                raise GlobalException.NotFound(detail="Message not found")
            
            for key, value in message.model_dump(exclude_unset=True).items():
                setattr(updated_message, key, value)
            
            await session.commit()
            await session.refresh(updated_message)

            updated_message = MessageInDB().model_validate(updated_message, from_attributes=True).model_dump()

            return {
                "message": "Message updated successfully",
                "data": updated_message
            }

        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))

    @staticmethod
    async def delete_message(session: AsyncSession, message_id: int):
        try:
            message = session.get(MessageModel, message_id)
            if not message:
                raise GlobalException.NotFound(detail="Message not found")

            session.delete(message)
            await session.commit()

            return {
                "message": "Message deleted successfully"
            }
        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))