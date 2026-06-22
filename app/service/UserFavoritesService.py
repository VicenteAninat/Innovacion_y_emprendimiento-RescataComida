from typing import List
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity
from app.repository.UserFavoritesRepository import UserFavoritesRepository

class UserFavoritesService:
    def __init__(self):
        self.user_favorites_repository = UserFavoritesRepository()

    def add_favorite(self, user_id: str, business_id: int) -> UserFavoritesEntity:
        return self.user_favorites_repository.add_favorite(user_id, business_id)

    def remove_favorite(self, user_id: str, business_id: int) -> bool:
        return self.user_favorites_repository.remove_favorite(user_id, business_id)

    def is_favorite(self, user_id: str, business_id: int) -> bool:
        return self.user_favorites_repository.is_favorite(user_id, business_id)

    def get_favorites_by_user(self, user_id: str) -> List[BusinessesEntity]:
        return self.user_favorites_repository.get_favorites_by_user(user_id)
