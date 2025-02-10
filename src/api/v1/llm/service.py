import asyncio
from openai import AsyncOpenAI
from src.config import settings

class LLMService:
    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)

    
    async def get_response(self, prompt: str):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content



llm_service = LLMService(settings.openai_api_key)
