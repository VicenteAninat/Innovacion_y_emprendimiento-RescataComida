from app.entity.FoodBanksEntity import FoodBanksEntity
from .BaseRepository import BaseRepository

class FoodBanksRepository(BaseRepository[FoodBanksEntity]):
    def __init__(self):
        super().__init__(FoodBanksEntity, "food_banks")
