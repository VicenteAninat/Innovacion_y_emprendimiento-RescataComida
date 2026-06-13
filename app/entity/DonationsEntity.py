from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .FoodBanksEntity import FoodBanksEntity

class DonationsEntity(BaseModel):
    id: Optional[int] = None
    business_id: int
    food_bank_id: int
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    tax_deductible_receipt_url: Optional[str] = None
    donated_at: Optional[datetime] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
    food_bank: Optional[FoodBanksEntity] = None
