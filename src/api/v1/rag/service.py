import asyncio
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import AsyncOpenAI
from src.config import settings
from datetime import datetime
from .utils import RAGUtils
from .exeptions import RAGException
from src.exeptions import GlobalException

class RAGService:
    def __init__(self, openai_api_key: str = settings.openai_api_key, pinecone_api_key: str = settings.pinecone_api_key, index_name: str = settings.pinecone_index_name):
        self.pinecone = Pinecone(api_key=pinecone_api_key)
        self.index = self.pinecone.Index(name=index_name)
        self.openai = AsyncOpenAI(api_key=openai_api_key)
    
    def get_index(self):
        return self.index
    
    async def get_embeddings(self, text: str):
        try:
            response = await self.openai.embeddings.create(input=text, model="text-embedding-ada-002")
            return response.data[0].embedding
        except Exception as e:
            raise GlobalException.InternalServerError(detail=str(e))
    
    async def upsert_embeddings(self, text: str):
        try:
            embedding = await self.get_embeddings(text)

            vectors = [{
                "values": embedding,
                "id": RAGUtils.get_hash(text),
                "metadata": {
                    "message": text,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }]

            await asyncio.to_thread(self.index.upsert, vectors=vectors, namespace="default")
            return {"message": "Embeddings upserted successfully"}
        except Exception as e:
            raise RAGException.EmbeddingsUpsertError(detail=str(e))
    
    async def search_embeddings(self, text: str):
        try:
            embedding = await self.get_embeddings(text)

            result = await asyncio.to_thread(
                self.index.query,
                vector=embedding,
                top_k=6,
                namespace="default",
                include_metadata=True
            )

            formatted_result = {
                "messages": [
                    {
                        "id": r["id"],
                        "score": r["score"],
                        "metadata": r["metadata"]
                    }
                    for r in result["matches"]
                ]
            }

            return formatted_result
        except Exception as e:
            raise GlobalException.NotFound(detail=str(e))

    

rag_service = RAGService()