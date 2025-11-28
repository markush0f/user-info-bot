import httpx
from app.config import HEADLESSX_API, HEADLESSX_AUTH_TOKEN
from app.logger import logger
from app.services.entity_service import EntityService
from app.services.user_service import UserService


async def extract_web_info(url: str):
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            r = await client.get(
                f"{HEADLESSX_API}/content",
                params={"token": HEADLESSX_AUTH_TOKEN, "url": url},
            )
            return {"content": r.text}
    except httpx.ReadTimeout:
        return {"error": "ReadTimeout while requesting external API"}
    except Exception as e:
        return {"error": str(e)}


