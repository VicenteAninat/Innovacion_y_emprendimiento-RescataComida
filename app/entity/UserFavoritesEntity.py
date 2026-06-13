from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserFavoritesEntity(BaseModel):
    user_id: int
    business_id: int
    created_at: Optional[datetime] = None
