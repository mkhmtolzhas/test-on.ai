import httpx
from .exeptions import LLMException
import asyncio
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone.grpc.index_grpc import GRPCIndex
from openai import AsyncOpenAI
from .config import settings as llm_settings
from datetime import datetime

class LLMUtils:
    @staticmethod
    async def send_callback(callback_url: str, response: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(callback_url, json=response)
                print(response)
        except Exception as e:
            raise LLMException.FailedCallbck(detail=str(e))
        
    

class PineconeService:
    def __init__(self, openai: AsyncOpenAI = llm_settings.openai, pinecone: Pinecone = llm_settings.pinecone, index: GRPCIndex = llm_settings.pinecone_index):
        self.pinecone = pinecone
        self.index = index
        self.openai = openai
    
    def get_index(self):
        return self.index
    
    async def get_embeddings(self, text: str):
        response = await self.openai.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    
    async def upsert_embeddings(self, text: str):
        embedding = await self.get_embeddings(text)
        asyncio.to_thread(
            self.index.upsert(
                vectors=[{
                    "values": embedding,
                    "id": text[:20],
                    "metadata": {
                        "message": text,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }],
                namespace="default",
            )
        )
    
    async def search_embeddings(self, text: str):
        embedding = await self.get_embeddings(text)
        asyncio.to_thread(
            self.index.query(
                vectors=embedding,
                namespace="default",
                top_k=3,
                include_metadata=True
            )
        )
    

pinecone_service = PineconeService()