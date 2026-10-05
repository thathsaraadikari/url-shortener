from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl
    expires_at: Optional[datetime] = None


class URLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str


class ClickInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    clicked_at: datetime
    user_agent: Optional[str] = None


class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    total_clicks: int
    recent_clicks: List[ClickInfo]