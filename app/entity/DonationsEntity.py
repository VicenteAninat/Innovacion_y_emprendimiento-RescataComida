"""Donations Entity.

This module defines the database representation schema for donations.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .BusinessesEntity import BusinessesEntity
    from .FoodBanksEntity import FoodBanksEntity

class DonationsEntity(BaseModel):
    """Represents a donation record in the system.

    Attributes:
        id (Optional[int]): Unique identifier for the donation record.
        business_id (int): Foreign key referring to the business making the donation.
        food_bank_id (int): Foreign key referring to the recipient food bank.
        description (Optional[str]): Description of items donated.
        weight_kg (Optional[float]): Estimated weight of food in kilograms.
        tax_deductible_receipt_url (Optional[str]): URL to access/download the receipt document.
        donated_at (Optional[datetime]): Timestamp when the donation was completed.
        business (Optional[BusinessesEntity]): Related business entity.
        food_bank (Optional[FoodBanksEntity]): Related food bank entity.
    """
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
