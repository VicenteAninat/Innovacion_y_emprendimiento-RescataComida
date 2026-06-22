from typing import Optional, List
from app.repository.UserRepository import UserRepository
from app.entity.UserEntity import UserEntity
from app.service.ReservationsService import ReservationsService
from app.config.supabase_client import supabase

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.reservations_service = ReservationsService()

    def get_users(self) -> List[UserEntity]:
        return self.user_repository.get_all()

    def get_user_byid(self, user_id: str) -> Optional[UserEntity]:
        return self.user_repository.get_by_id(user_id, "id")

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        return self.user_repository.get_by_email(email)

    def get_user_reservations(self, user_id: str):
        return self.reservations_service.get_reservations_by_user_id(user_id)


    def register(self, email: str, password: str, name: Optional[str] = None, phone: Optional[str] = None, role: str = "customer", business_id: Optional[int] = None) -> UserEntity:
        # 1. Registrar en Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            raise Exception("No se pudo registrar el usuario en Supabase Auth.")
            
        # 2. Guardar perfil en la tabla pública 'users'
        user_entity = UserEntity(
            id=auth_response.user.id,
            name=name,
            email=email,
            phone=phone,
            role=role,
            business_id=business_id
        )
        return self.user_repository.create(user_entity)

    def login(self, email: str, password: str) -> dict:
        # 1. Iniciar sesión en Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if not auth_response.session:
            raise Exception("Credenciales inválidas.")
            
        # 2. Obtener perfil con rol
        user_profile = self.get_user_byid(auth_response.user.id)
        
        return {
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token,
            "expires_in": auth_response.session.expires_in,
            "token_type": auth_response.session.token_type,
            "user": user_profile
        }
    def update_user(self, user_id: str, update_data: dict) -> Optional[UserEntity]:
        return self.user_repository.update(user_id, update_data, "id")