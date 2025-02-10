from pydantic import BaseModel

class LLMRequestSchema(BaseModel):
    message: str
    callback_url: str

class LLMResponseSchema(BaseModel):
    response: str