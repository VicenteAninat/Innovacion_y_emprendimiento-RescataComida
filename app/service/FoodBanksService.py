from typing import List, Optional
from app.entity.FoodBanksEntity import FoodBanksEntity
from app.repository.FoodBanksRepository import FoodBanksRepository

class FoodBanksService:
    def __init__(self):
        self.food_banks_repository = FoodBanksRepository()

    def get_all_food_banks(self) -> List[FoodBanksEntity]:
        return self.food_banks_repository.get_all()

    def get_food_bank_by_id(self, id_val: int) -> Optional[FoodBanksEntity]:
        return self.food_banks_repository.get_by_id(id_val)

    def create_food_bank(self, rut: str, name: Optional[str] = None, contact_email: Optional[str] = None, contact_phone: Optional[str] = None, address: Optional[str] = None) -> FoodBanksEntity:
        entity = FoodBanksEntity(
            rut=rut,
            name=name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            address=address
        )
        return self.food_banks_repository.create(entity)

    def update_food_bank(self, id_val: int, data: dict) -> Optional[FoodBanksEntity]:
        return self.food_banks_repository.update(id_val, data)

    def delete_food_bank(self, id_val: int) -> bool:
        return self.food_banks_repository.delete(id_val)
