from typing import List
from app.entity.ReviewsEntity import ReviewsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class ReviewsRepository(BaseRepository[ReviewsEntity]):
    def __init__(self):
        super().__init__(ReviewsEntity, "reviews")

    def get_by_business_id(self, business_id: int) -> List[ReviewsEntity]:
        # Obtiene las reseñas del local e incluye los datos del usuario que la escribió
        response = (
            supabase.table(self.table_name)
            .select("*, user(*)")
            .eq("business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]
