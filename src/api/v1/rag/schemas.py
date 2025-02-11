from pydantic import BaseModel

class RAGRequest(BaseModel):
    text: str

    class Config:
        from_attributes = True