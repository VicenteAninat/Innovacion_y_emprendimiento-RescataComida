from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity

class MlHistoricalDataEntity(BaseModel):
    id: Optional[int] = None
    business_id: int
    date: Optional[date] = None
    hour: Optional[int] = None
    weather_condition: Optional[str] = None
    surplus_kg: Optional[float] = None
    sold_bags: Optional[int] = None
    wasted_bags: Optional[int] = None
    dynamic_pricing_suggested: Optional[float] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
