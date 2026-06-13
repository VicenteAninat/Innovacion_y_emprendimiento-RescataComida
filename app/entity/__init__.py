from .UserEntity import UserEntity
from .BusinessesEntity import BusinessesEntity
from .OffersEntity import OffersEntity
from .FoodBanksEntity import FoodBanksEntity
from .ReservationsEntity import ReservationsEntity
from .ReviewsEntity import ReviewsEntity
from .MlHistoricalDataEntity import MlHistoricalDataEntity
from .DonationsEntity import DonationsEntity
from .UserFavoritesEntity import UserFavoritesEntity

# Rebuild Pydantic models to resolve forward references in type annotations
UserEntity.model_rebuild()
BusinessesEntity.model_rebuild()
OffersEntity.model_rebuild()
FoodBanksEntity.model_rebuild()
ReservationsEntity.model_rebuild()
ReviewsEntity.model_rebuild()
MlHistoricalDataEntity.model_rebuild()
DonationsEntity.model_rebuild()

__all__ = [
    "UserEntity",
    "BusinessesEntity",
    "OffersEntity",
    "FoodBanksEntity",
    "ReservationsEntity",
    "ReviewsEntity",
    "MlHistoricalDataEntity",
    "DonationsEntity",
    "UserFavoritesEntity",
]
