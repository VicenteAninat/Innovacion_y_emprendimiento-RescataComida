from typing import List
from app.entity.DonationsEntity import DonationsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class DonationsRepository(BaseRepository[DonationsEntity]):
    def __init__(self):
        super().__init__(DonationsEntity, "donations")

    def get_by_business_id(self, business_id: int) -> List[DonationsEntity]:
        # Carga la donación con el banco de alimentos asociado
        response = (
            supabase.table(self.table_name)
            .select("*, food_bank(*)")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
