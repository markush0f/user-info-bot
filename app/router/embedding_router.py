from fastapi import APIRouter
import uuid

from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


@router.post("/{user_id}/process_embeddings")
def process_user_embeddings(user_id: str):
    service = EmbeddingService()
    result = service.process_user(uuid.UUID(user_id))
    return result
