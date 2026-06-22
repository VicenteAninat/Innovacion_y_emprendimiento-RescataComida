from typing import Optional
from app.entity.UserEntity import UserEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class UserRepository(BaseRepository[UserEntity]):
    def __init__(self):
        super().__init__(UserEntity, "users")

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        response = supabase.table(self.table_name).select("*").eq("email", email).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def get_user_with_business(self, user_id: str) -> Optional[UserEntity]:
        # Trae la información del usuario y su comercio asociado anidado
        response = supabase.table(self.table_name).select("*, business(*)").eq("id", user_id).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])
