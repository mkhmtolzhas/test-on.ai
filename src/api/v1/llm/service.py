from openai import AsyncOpenAI, OpenAIError, RateLimitError, BadRequestError
from src.exeptions import GlobalException
from .schemas import LLMRequestSchema, LLMResponseSchema
from .exeptions import LLMException
from src.config import settings

class LLMService:
    def __init__(self, openai_api_key: str = settings.openai_api_key):
        self.client = AsyncOpenAI(api_key=openai_api_key)

    
    async def get_response(self, prompt: LLMRequestSchema) -> LLMResponseSchema:
        if not prompt.message:
            raise GlobalException.UnprocessableEntity(detail="message is required")
        
        if not prompt.callback_url:
            raise GlobalException.UnprocessableEntity(detail="callback_url is required")

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt.message},
                ],
            )

            if not response or not response.choices or not response.choices[0].message:
                raise LLMException.APIError(detail="Invalid response from OpenAI")

            return LLMResponseSchema(response=response.choices[0].message.content)

        except BadRequestError as e:
            raise GlobalException.UnprocessableEntity(detail=f"Bad request: {str(e)}")
        except RateLimitError as e:
            raise GlobalException.TooManyRequests(detail=f"Rate limit exceeded: {str(e)}")
        except OpenAIError as e:
            raise LLMException.APIError(detail=f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise GlobalException.InternalServerError(detail=f"Internal server error: {str(e)}")



llm_service = LLMService()
