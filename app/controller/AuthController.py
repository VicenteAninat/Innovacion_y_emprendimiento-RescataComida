"""Authentication Controller.

This module handles authentication endpoints, request schemas, security
dependencies, and registration/profile operations.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.service.UserService import UserService
from app.entity.UserEntity import UserEntity
from app.entity.ReservationsEntity import ReservationsEntity
from app.config.supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Authentication"])
user_service = UserService()

# Pydantic Schemas for Requests
class RegisterRequest(BaseModel):
    """Request schema for user registration.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
        name (Optional[str]): The user's full name.
        phone (Optional[str]): The user's phone number.
        role (Optional[str]): The user's role (customer, worker, admin).
        business_id (Optional[int]): The business ID associated if role is worker.
    """
    email: EmailStr
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "customer"
    business_id: Optional[int] = None

class LoginRequest(BaseModel):
    """Request schema for user login.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UpdateProfileRequest(BaseModel):
    """Request schema for updating a user's profile.

    Attributes:
        name (Optional[str]): The updated name of the user.
        phone (Optional[str]): The updated phone number of the user.
    """
    name: Optional[str] = None
    phone: Optional[str] = None

# Endpoints
@router.post("/register", response_model=UserEntity)
def register(req: RegisterRequest):
    """Registra un nuevo usuario en el sistema.

    Crea las credenciales en Supabase Auth y genera el perfil local en la tabla 'users'
    con el rol asignado ('customer', 'worker', o 'admin').

    Args:
        req (RegisterRequest): The registration request data.

    Returns:
        UserEntity: The newly registered user profile.

    Raises:
        HTTPException: If the role is invalid or registration fails.
    """
    try:
        if req.role not in ["customer", "worker", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'customer', 'worker', or 'admin'")
            
        new_user = user_service.register(
            email=req.email,
            password=req.password,
            name=req.name,
            phone=req.phone,
            role=req.role,
            business_id=req.business_id
        )
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(req: LoginRequest):
    """Inicia sesión en la plataforma utilizando email y contraseña.

    Retorna tokens de acceso y refresco de Supabase, expiración y perfil completo del usuario.

    Args:
        req (LoginRequest): The login credentials.

    Returns:
        dict: A dictionary containing access/refresh tokens and user profile information.

    Raises:
        HTTPException: If credentials are invalid or login fails.
    """
    try:
        result = user_service.login(email=req.email, password=req.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Security Dependencies
def get_current_user(authorization: str = Header(...)):
    """Extracts and verifies the current authenticated Supabase user from the Authorization header.

    Args:
        authorization (str): The Authorization header containing the Bearer token.

    Returns:
        User: The Supabase user object.

    Raises:
        HTTPException: If the token format is invalid or token verification fails.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Token format. Must be Bearer <token>")
    token = authorization.split(" ")[1]
    
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired session.")
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth error: {str(e)}")

def get_current_user_profile(user=Depends(get_current_user)) -> UserEntity:
    """Retrieves the local user profile entity for the authenticated Supabase user.

    Args:
        user: The authenticated Supabase user.

    Returns:
        UserEntity: The local database profile entity.

    Raises:
        HTTPException: If the profile is not found.
    """
    profile = user_service.get_user_byid(user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found in database.")
    return profile

def require_roles(allowed_roles: list[str]):
    """Returns a dependency function that enforces user roles.

    Args:
        allowed_roles (list[str]): The list of roles allowed to access the resource.

    Returns:
        function: The role verification dependency.
    """
    def role_verifier(profile: UserEntity = Depends(get_current_user_profile)):
        """Verifies if the current user profile has one of the allowed roles.

        Args:
            profile (UserEntity): The current user's profile.

        Returns:
            UserEntity: The verified profile.

        Raises:
            HTTPException: If the user role is not allowed.
        """
        if profile.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permissions to access this resource.")
        return profile
    return role_verifier

@router.get("/profile", response_model=UserEntity)
def get_profile(current_user: UserEntity = Depends(get_current_user_profile)):
    """Obtiene el perfil del usuario actualmente autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): The profile of the authenticated user.

    Returns:
        UserEntity: The current user's profile details.
    """
    return current_user

@router.patch("/profile", response_model=UserEntity)
def update_profile(req: UpdateProfileRequest, current_user: UserEntity = Depends(get_current_user_profile)):
    """Actualiza parcialmente el perfil del usuario actualmente autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        req (UpdateProfileRequest): The partial profile update fields.
        current_user (UserEntity): The profile of the authenticated user.

    Returns:
        UserEntity: The updated user profile.

    Raises:
        HTTPException: If no fields are provided or update fails.
    """    
    try:
        update_dict = req.dict(exclude_unset=True)
        if not update_dict:
            raise HTTPException(status_code=400, detail="No se enviaron campos válidos para actualizar.")
            
        updated_user = user_service.update_user(current_user.id, update_dict)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar.")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations", response_model=List[ReservationsEntity])
def get_user_reservations(current_user: UserEntity = Depends(get_current_user)):
    """Obtiene las reservas del usuario autenticado.

    Args:
        current_user (UserEntity): The authenticated Supabase user.

    Returns:
        List[ReservationsEntity]: A list of reservations belonging to the user.

    Raises:
        HTTPException: If retrieval fails.
    """
    id_user=current_user.id
    try:
        user_reservations = user_service.get_user_reservations(id_user)
        return user_reservations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class LinkWorkerRequest(BaseModel):
    user_id: str
    business_id: int

@router.post("/link-worker", response_model=UserEntity)
def link_worker(req: LinkWorkerRequest, current_user: UserEntity = Depends(get_current_user_profile)):
    """Vincula a un usuario con rol 'worker' a un local comercial (business_id).

    Permitido para administradores globales o trabajadores del mismo local.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        req (LinkWorkerRequest): Schema containing user_id and business_id.
        current_user (UserEntity): Profile of the authenticated caller.

    Returns:
        UserEntity: The updated worker profile.

    Raises:
        HTTPException: If caller lacks permissions (403) or target is invalid (400).
    """
    try:
        return user_service.link_worker(
            target_user_id=req.user_id,
            target_business_id=req.business_id,
            caller_user_id=str(current_user.id),
            caller_role=current_user.role,
            caller_business_id=current_user.business_id
        )
    except ValueError as ve:
        error_msg = str(ve)
        if "permiso" in error_msg.lower():
            raise HTTPException(status_code=403, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
