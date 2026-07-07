"""Food Banks Entity.

This module defines the database representation schema for food banks.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .DonationsEntity import DonationsEntity

class FoodBanksEntity(BaseModel):
    """Represents a food bank organization in the system.

    Attributes:
        id (Optional[int]): Unique identifier for the food bank.
        rut (str): Tax identification number/RUT.
        name (Optional[str]): Commercial/official name.
        contact_email (Optional[str]): Contact email address.
        contact_phone (Optional[str]): Contact phone number.
        address (Optional[str]): Physical street address.
        created_at (Optional[datetime]): Timestamp when the record was created.
        donations (Optional[List[DonationsEntity]]): List of donations received by the bank.
    """
    id: Optional[int] = None
    rut: str
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    # Fields for joined relations
    donations: Optional[List[DonationsEntity]] = None
