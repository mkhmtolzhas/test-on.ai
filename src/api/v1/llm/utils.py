import httpx

class LLMUtils:
    @staticmethod
    async def send_callback(callback_url: str, response: dict):
        try:
            async with httpx.AsyncClient() as client:
                await client.post(callback_url, json=response)
        except Exception as e:
            print(e)