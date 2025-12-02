from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
import httpx
from app.core.db import get_session
from app.domains.entities.schemas.save_entity_request import (
    SaveEntityNoGithubProjectRequest,
)
from app.domains.entities.service import EntityService

router = APIRouter(prefix="/entity", tags=["entities"])


@router.get("/health")
async def health():
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get("http://localhost:3001/api/health")
        return {"content": r.json()}


@router.get("/")
async def extract_web_information(
    url: str,
    session: Session = Depends(get_session),
):
    service = EntityService(session)
    return await service.get_web_info(url)


@router.post("/")
def create_entity_endpoint(
    data: SaveEntityNoGithubProjectRequest,
    session: Session = Depends(get_session),
):
    service = EntityService(session)

    entity = service.create_entity(
        user_id=data.user_id,
        project_id=None,
        entity_type=data.type,
        raw_data=data.raw_data,
        summary=data.summary,
    )

    return {"entity": entity, "status": "saved"}
