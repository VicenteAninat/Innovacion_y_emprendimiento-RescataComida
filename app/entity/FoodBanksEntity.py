from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .DonationsEntity import DonationsEntity

class FoodBanksEntity(BaseModel):
    id: Optional[int] = None
    rut: str
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    donations: Optional[List[DonationsEntity]] = None
