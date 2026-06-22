from typing import List, Optional
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class UserFavoritesRepository(BaseRepository[UserFavoritesEntity]):
    def __init__(self):
        super().__init__(UserFavoritesEntity, "user_favorites")

    def add_favorite(self, user_id: str, business_id: int) -> UserFavoritesEntity:
        entity = UserFavoritesEntity(user_id=user_id, business_id=business_id)
        return self.create(entity)

    def remove_favorite(self, user_id: str, business_id: int) -> bool:
        response = (
            supabase.table(self.table_name)
            .delete()
            .eq("user_id", user_id)
            .eq("business_id", business_id)
            .execute()
        )
        return len(response.data) > 0

    def is_favorite(self, user_id: str, business_id: int) -> bool:
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq("user_id", user_id)
            .eq("business_id", business_id)
            .execute()
        )
        return len(response.data) > 0

    def get_favorites_by_user(self, user_id: str) -> List[BusinessesEntity]:
        # Carga la lista de favoritos de un usuario e incluye los comercios
        response = (
            supabase.table(self.table_name)
            .select("*, business(*)")
            .eq("user_id", user_id)
            .execute()
        )
        # Extrae la lista de comercios asociados
        favorites = []
        for item in response.data:
            if item.get("business"):
                favorites.append(BusinessesEntity(**item["business"]))
        return favorites
