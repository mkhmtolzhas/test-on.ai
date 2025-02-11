from fastapi import APIRouter
from .schemas import LLMRequestSchema, LLMResponseSchema
from .service import llm_service
from .utils import LLMUtils

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.post("/get_response", response_model=LLMResponseSchema)
async def get_response(body: LLMRequestSchema):

    response = await llm_service.get_response(body)
    # await LLMUtils.send_callback(body.callback_url, response.model_dump())
    await LLMUtils.send_to_message_service(body.message)
    return response



