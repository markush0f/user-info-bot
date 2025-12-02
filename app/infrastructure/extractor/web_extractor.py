
import httpx
from app.core.config import HEADLESSX_API, HEADLESSX_AUTH_TOKEN


async def extract_web_info( url: str):
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