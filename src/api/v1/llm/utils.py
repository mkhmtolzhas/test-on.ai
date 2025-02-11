import httpx
from .exeptions import LLMException
from src.config import settings

class LLMUtils:
    @staticmethod
    async def send_callback(callback_url: str, response: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(callback_url, json=response)
        except Exception as e:
            raise LLMException.FailedCallbck(detail=str(e))

        
    @staticmethod
    async def get_context(message: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{settings.host}/api/v1/rag/search_embeddings", json={"text": message})
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
        except Exception as e:
            raise LLMException.FailedCallbck(detail=str(e))
    
    @staticmethod
    async def upsert_context(message: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{settings.host}/api/v1/rag/upsert_embeddings", json={"text": message})
                return {
                    "status": response.status_code,
                    "data": response.json()
                }
        except Exception as e:
            raise LLMException.FailedCallbck(detail=str(e))
        