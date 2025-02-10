from openai import AsyncOpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from src.config import settings


class Config:
    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.openai_api_key)
        self.pinecone = Pinecone(api_key=settings.pinecone_api_key)
        self.pinecone_index = self.pinecone.Index(name=settings.pinecone_index_name)


settings = Config()