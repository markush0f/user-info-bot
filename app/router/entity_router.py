from fastapi import APIRouter, HTTPException
import httpx
from app.models.schemas.save_entity_request import SaveEntityNoGithubProjectRequest
from app.services.entity_service import EntityService
from app.utils.extract_web_info import extract_web_info

router = APIRouter(prefix="/entity", tags=["entities"])


@router.get("/health")
async def health():
    # http://localhost:3001/api/health
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(
            "http://localhost:3001/api/health",
        )
        return {"content": r.json()}


@router.get("/")
async def extract_web_information(url: str):
    return await extract_web_info(url)


@router.post("/")
def create_entity_endpoint(data: SaveEntityNoGithubProjectRequest):
    service = EntityService()

    entity = service.create_entity(
        user_id=data.user_id,
        project_id=None,
        entity_type=data.type,
        raw_data=data.raw_data,
        summary=data.summary,
    )

    return {"entity_id": entity.id, "status": "saved"}
