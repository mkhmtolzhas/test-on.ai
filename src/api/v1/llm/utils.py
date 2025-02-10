import httpx
from .exeptions import LLMException

class LLMUtils:
    @staticmethod
    async def send_callback(callback_url: str, response: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(callback_url, json=response)
        except Exception as e:
            raise LLMException.FailedCallbck(detail=str(e))
        