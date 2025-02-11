from fastapi import APIRouter
from .llm.router import router as llm_router
from .message.router import router as message_router
from .rag.router import router as rag_router

router = APIRouter(prefix="/v1")

router.include_router(llm_router)
router.include_router(message_router)
router.include_router(rag_router)


