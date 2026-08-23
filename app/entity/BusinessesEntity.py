"""Businesses Entity.

This module defines the database representation schema for businesses.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Union, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .UserEntity import UserEntity
    from .OffersEntity import OffersEntity
    from .ReviewsEntity import ReviewsEntity
    from .MlHistoricalDataEntity import MlHistoricalDataEntity
    from .DonationsEntity import DonationsEntity

class BusinessesEntity(BaseModel):
    """Represents a business entity in the system.

    Attributes:
        id (Optional[int]): The primary key identifier of the business.
        rut (str): The unique tax/commercial RUT identifier.
        name (Optional[str]): The business's name.
        category (Optional[str]): The category/type of commercial activity.
        address (Optional[str]): Physical street address.
        location (Optional[str]): Geographical point (WKT or PostGIS geometry text).
        is_premium (bool): Premium membership status. Defaults to False.
        created_at (Optional[datetime]): Timestamp of record creation.
        users (Optional[List[UserEntity]]): Related users (workers, admins).
        offers (Optional[List[OffersEntity]]): Offers published by this business.
        reviews (Optional[List[ReviewsEntity]]): Reviews written about this business.
        ml_historical_data (Optional[List[MlHistoricalDataEntity]]): Historical sales/predictions.
        donations (Optional[List[DonationsEntity]]): Surplus food donations history.
        favorited_by_users (Optional[List[UserEntity]]): Users who favorited this business.
    """
    id: Optional[int] = None
    rut: str
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    # PostGIS devuelve la geometría como GeoJSON (dict) o WKT (str)
    location: Optional[Union[str, dict]] = None
    is_premium: bool = False
    created_at: Optional[datetime] = None

    # Fields for joined relations
    users: Optional[List[UserEntity]] = None
    offers: Optional[List[OffersEntity]] = None
    reviews: Optional[List[ReviewsEntity]] = None
    ml_historical_data: Optional[List[MlHistoricalDataEntity]] = None
    donations: Optional[List[DonationsEntity]] = None
    favorited_by_users: Optional[List[UserEntity]] = None
