"""Food Banks Repository.

This module defines the FoodBanksRepository class which extends BaseRepository for managing food bank organizations.
"""

from app.entity.FoodBanksEntity import FoodBanksEntity
from .BaseRepository import BaseRepository

class FoodBanksRepository(BaseRepository[FoodBanksEntity]):
    """Repository class managing database operations on the 'food_banks' table."""

    def __init__(self):
        """Initializes the repository targeting the 'food_banks' table."""
        super().__init__(FoodBanksEntity, "food_banks")
