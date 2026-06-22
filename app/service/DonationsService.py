from typing import List, Optional
from app.entity.DonationsEntity import DonationsEntity
from app.repository.DonationsRepository import DonationsRepository

class DonationsService:
    def __init__(self):
        self.donations_repository = DonationsRepository()

    def get_all_donations(self) -> List[DonationsEntity]:
        return self.donations_repository.get_all()

    def get_donation_by_id(self, id_val: int) -> Optional[DonationsEntity]:
        return self.donations_repository.get_by_id(id_val)

    def get_donations_by_business(self, business_id: int) -> List[DonationsEntity]:
        return self.donations_repository.get_by_business_id(business_id)

    def create_donation(self, business_id: int, food_bank_id: int, description: Optional[str] = None, weight_kg: Optional[float] = None, tax_deductible_receipt_url: Optional[str] = None) -> DonationsEntity:
        entity = DonationsEntity(
            business_id=business_id,
            food_bank_id=food_bank_id,
            description=description,
            weight_kg=weight_kg,
            tax_deductible_receipt_url=tax_deductible_receipt_url
        )
        return self.donations_repository.create(entity)

    def update_donation(self, id_val: int, data: dict) -> Optional[DonationsEntity]:
        return self.donations_repository.update(id_val, data)

    def delete_donation(self, id_val: int) -> bool:
        return self.donations_repository.delete(id_val)