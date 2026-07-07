"""Offers Entity.

This module defines the database representation schema for surprise bag offers.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .ReservationsEntity import ReservationsEntity

class OffersEntity(BaseModel):
    """Represents a surprise bag or food discount offer in the database.

    Attributes:
        id (Optional[int]): Unique identifier for the offer.
        business_id (int): Foreign key referring to the associated business.
        title (str): Name/title of the offer.
        description (Optional[str]): Detailed description of what might be in the surprise bag.
        original_price (float): Original retail price.
        discounted_price (float): Discounted selling price.
        quantity_available (int): Quantity of items in stock. Defaults to 1.
        pickup_start_time (datetime): Pickup start window.
        pickup_end_time (datetime): Pickup end window.
        status (str): Offer status (active, completed, cancelled). Defaults to "active".
        kg_saved_per_unit (Optional[float]): Quantity of food in kg saved per bag unit.
        co2_avoided_per_unit (Optional[float]): Estimated greenhouse emissions avoided in kg CO2.
        created_at (Optional[datetime]): Timestamp when the offer was created.
        business (Optional[BusinessesEntity]): Related business entity details.
        reservations (Optional[List[ReservationsEntity]]): Reservations made for this offer.
    """
    id: Optional[int] = None
    business_id: int
    title: str
    description: Optional[str] = None
    original_price: float
    discounted_price: float
    quantity_available: int = 1
    pickup_start_time: datetime
    pickup_end_time: datetime
    status: str = "active"
    kg_saved_per_unit: Optional[float] = None
    co2_avoided_per_unit: Optional[float] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    business: Optional[BusinessesEntity] = None
    reservations: Optional[List[ReservationsEntity]] = None
