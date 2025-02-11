from datetime import datetime
from pydantic import BaseModel

class MessageCreate(BaseModel):
    message: str

    class Config:
        from_attributes = True



class MessageInDB(MessageCreate):
    id: int
    created_at: datetime

