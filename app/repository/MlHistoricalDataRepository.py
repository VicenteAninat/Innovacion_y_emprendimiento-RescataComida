from typing import List
from app.entity.MlHistoricalDataEntity import MlHistoricalDataEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class MlHistoricalDataRepository(BaseRepository[MlHistoricalDataEntity]):
    def __init__(self):
        super().__init__(MlHistoricalDataEntity, "ml_historical_data")

    def get_by_business_id(self, business_id: int) -> List[MlHistoricalDataEntity]:
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
