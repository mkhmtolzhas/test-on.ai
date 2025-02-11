from fastapi import APIRouter
from .service import rag_service
from .schemas import RAGRequest


router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/search_embeddings")
async def search_embeddings(body: RAGRequest):
    embeddings = await rag_service.search_embeddings(body.text)
    return embeddings


@router.post("/upsert_embeddings")
async def upsert_embeddings(body: RAGRequest):
    return await rag_service.upsert_embeddings(body.text)


