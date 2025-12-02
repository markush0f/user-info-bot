from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid
from app.core.db import get_session
from app.domains.embeddings.service import EmbeddingService

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


@router.post("/{user_id}/process_embeddings")
def process_user_embeddings(
    user_id: str,
    session: Session = Depends(get_session),
):
    # Added: inject session into EmbeddingService
    service = EmbeddingService(session)
    return service.process_user(uuid.UUID(user_id))
