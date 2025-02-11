from fastapi import APIRouter, HTTPException
from .service import MessageService
from .schemas import MessageCreate, MessageInDB
from src.database import SessionDep

router = APIRouter(prefix='/message')

@router.post("/")
async def create_message(message: MessageCreate, session: SessionDep = SessionDep()):
    return await MessageService.create_message(session, message)

@router.get("/")
async def get_messages(page: int = 1, limit: int = 10, session: SessionDep = SessionDep()):
    return await MessageService.get_messages(session, page, limit)

@router.get("/{message_id}")
async def get_message(message_id: int, session: SessionDep = SessionDep()):
    return await MessageService.get_message(session, message_id)

@router.put("/{message_id}")
async def update_message(message_id: int, message: MessageCreate, session: SessionDep = SessionDep()):
    return await MessageService.update_message(session, message_id, message)

@router.delete("/{message_id}")
async def delete_message(message_id: int, session: SessionDep = SessionDep()):
    return await MessageService.delete_message(session, message_id)



