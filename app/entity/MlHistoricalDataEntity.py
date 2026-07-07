"""ML Historical Data Entity.

This module defines the database representation schema for machine learning historical data records.
"""

from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity

class MlHistoricalDataEntity(BaseModel):
    """Represents a record of historical sales/surplus data used for ML analysis and dynamic pricing.

    Attributes:
        id (Optional[int]): Unique identifier for the historical data row.
        business_id (int): Foreign key referring to the associated business.
        date (Optional[date]): Calendar date of the record.
        hour (Optional[int]): Time hour of the record (0-23).
        weather_condition (Optional[str]): Weather status during the recorded timeframe.
        surplus_kg (Optional[float]): Quantity of surplus food in kilograms.
        sold_bags (Optional[int]): Count of surprise bags sold.
        wasted_bags (Optional[int]): Count of surprise bags wasted/discarded.
        dynamic_pricing_suggested (Optional[float]): The price suggested by the pricing algorithm.
        business (Optional[BusinessesEntity]): Related business entity.
    """
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
