"""User Service.

This module defines the UserService class which handles registration, authentication, and profile management logic.
"""

from typing import Optional, List
from app.repository.UserRepository import UserRepository
from app.entity.UserEntity import UserEntity
from app.service.ReservationsService import ReservationsService
from app.config.supabase_client import supabase

class UserService:
    """Service class encapsulating authentication and user profile operations."""

    def __init__(self):
        """Initializes the service by setting up the UserRepository and ReservationsService."""
        self.user_repository = UserRepository()
        self.reservations_service = ReservationsService()

    def get_users(self) -> List[UserEntity]:
        """Retrieves a list of all registered users in the database.

        Returns:
            List[UserEntity]: A list of all user profiles.
        """
        return self.user_repository.get_all()

    def get_user_byid(self, user_id: str) -> Optional[UserEntity]:
        """Fetches a user profile by its unique ID.

        Args:
            user_id (str): UUID string of the user.

        Returns:
            Optional[UserEntity]: The user entity if found, otherwise None.
        """
        return self.user_repository.get_by_id(user_id, "id")

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """Fetches a user profile by email address.

        Args:
            email (str): Email address of the user.

        Returns:
            Optional[UserEntity]: The user entity if found, otherwise None.
        """
        return self.user_repository.get_by_email(email)

    def get_user_reservations(self, user_id: str):
        """Retrieves reservations created by a specific user.

        Args:
            user_id (str): UUID string of the customer.

        Returns:
            List[ReservationsEntity]: List of reservations.
        """
        return self.reservations_service.get_reservations_by_user_id(user_id)

    def register(self, email: str, password: str, name: Optional[str] = None, phone: Optional[str] = None, role: str = "customer", business_id: Optional[int] = None) -> UserEntity:
        """Registers a new user in both Supabase Auth and the local users table.

        Args:
            email (str): The email address of the user.
            password (str): The password.
            name (Optional[str]): User's full name.
            phone (Optional[str]): User's phone number.
            role (str): Role assigned to the user. Defaults to "customer".
            business_id (Optional[int]): Associated business ID if worker.

        Returns:
            UserEntity: The newly created user profile.

        Raises:
            Exception: If registration fails in Supabase Auth.
        """
        # 1. Registrar en Supabase Auth
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
        except Exception as e:
            error_msg = str(e)
            if "User already registered" in error_msg:
                raise Exception("El usuario ya está registrado.")
            raise Exception(f"Error de registro: {error_msg}")
        
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
        """Authenticates a user via Supabase Auth and returns the session tokens and local profile.

        Args:
            email (str): The email address.
            password (str): The password.

        Returns:
            dict: Session details including access_token, refresh_token, and user profile.

        Raises:
            Exception: If credentials are invalid.
        """
        # 1. Iniciar sesión en Supabase Auth
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        except Exception as e:
            error_msg = str(e)
            if "Invalid login credentials" in error_msg:
                raise Exception("Credenciales de inicio de sesión inválidas.")
            raise Exception(f"Error de autenticación: {error_msg}")
        
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
        """Updates user profile attributes.

        Args:
            user_id (str): UUID string of the user to update.
            update_data (dict): Dict of updated fields.

        Returns:
            Optional[UserEntity]: The updated user profile if found, otherwise None.
        """
        return self.user_repository.update(user_id, update_data, "id")

    def link_worker(self, target_user_id: str, target_business_id: int, caller_user_id: str, caller_role: str, caller_business_id: Optional[int]) -> UserEntity:
        """Links a user with the 'worker' role to a specific business ID.

        Args:
            target_user_id (str): UUID string of the worker to link.
            target_business_id (int): ID of the business.
            caller_user_id (str): UUID string of the user making the request.
            caller_role (str): Role of the caller ('admin' or 'worker').
            caller_business_id (Optional[int]): Business ID of the caller if worker.

        Returns:
            UserEntity: The updated worker profile.

        Raises:
            ValueError: If target user doesn't exist, target user is not a worker, or caller lacks permission.
        """
        # 1. Obtener perfil del usuario destino
        target_user = self.get_user_byid(target_user_id)
        if not target_user:
            raise ValueError("El usuario destino no existe.")
            
        # 2. Validar que el usuario destino sea 'worker'
        if target_user.role != "worker":
            raise ValueError("El usuario destino debe tener el rol de 'worker'. Registra un nuevo usuario con ese rol.")
            
        # 3. Validar permisos del llamador
        if caller_role != "admin":
            if caller_role != "worker":
                raise ValueError("No tienes permiso para realizar esta acción.")
            if caller_business_id != target_business_id:
                raise ValueError("No tienes permiso para vincular trabajadores a un local comercial ajeno.")
                
        # 4. Actualizar el business_id del usuario destino
        updated_user = self.update_user(target_user_id, {"business_id": target_business_id})
        if not updated_user:
            raise ValueError("No se pudo realizar la vinculación del trabajador.")
            
        return updated_user
