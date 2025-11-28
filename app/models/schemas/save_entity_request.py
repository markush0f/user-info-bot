import uuid
from pydantic import BaseModel
from typing import Any, Optional, Dict

class SaveEntityNoGithubProjectRequest(BaseModel):
    user_id: uuid.UUID
    type: str
    raw_data: Dict[str, Any]
    summary: str