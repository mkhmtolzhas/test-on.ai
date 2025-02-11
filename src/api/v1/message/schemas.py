from datetime import datetime
from pydantic import BaseModel

class MessageCreate(BaseModel):
    message: str



class MessageInDB(MessageCreate):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True
