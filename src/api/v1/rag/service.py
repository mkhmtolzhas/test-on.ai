import asyncio
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone.grpc.index_grpc import GRPCIndex
from openai import AsyncOpenAI
from src.config import settings
from datetime import datetime

class PineconeService:
    def __init__(self, openai_api_key: str = settings.openai_api_key, pinecone_api_key: str = settings.pinecone_api_key, index_name: str = settings.pinecone_index_name):
        self.pinecone = Pinecone(api_key=pinecone_api_key)
        self.index = self.pinecone.Index(name=index_name)
        self.openai = AsyncOpenAI(api_key=openai_api_key)
    
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