from fastapi import APIRouter

from src.exeptions import GlobalException
from .schemas import LLMRequestSchema, LLMResponseSchema
from .service import llm_service
from .utils import LLMUtils

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.post("/get_response", response_model=LLMResponseSchema)
async def get_response(body: LLMRequestSchema):

    context = await LLMUtils.get_context(body.message)
    if context["status"] != 200:
        raise GlobalException.InternalServerError(detail="Failed to retrieve context")
    

    upsert = await LLMUtils.upsert_context(body.message)
    if upsert["status"] != 200:
        raise GlobalException.InternalServerError(detail="Failed to upsert embeddings")

    response = await llm_service.get_response(body, context)
    await LLMUtils.send_callback(body.callback_url, response.model_dump())
    return response



