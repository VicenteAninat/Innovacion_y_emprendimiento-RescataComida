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
    email: EmailStr
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "customer"
    business_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

# Endpoints
@router.post("/register", response_model=UserEntity)
def register(req: RegisterRequest):
    """
    Registra un nuevo usuario en el sistema.
    Crea las credenciales en Supabase Auth y genera el perfil local en la tabla 'users'
    con el rol asignado ('customer', 'worker', o 'admin').
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
    """
    Inicia sesión en la plataforma utilizando email y contraseña.
    Retorna tokens de acceso y refresco de Supabase, expiración y perfil completo del usuario.
    """
    try:
        result = user_service.login(email=req.email, password=req.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Security Dependencies
def get_current_user(authorization: str = Header(...)):
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
    profile = user_service.get_user_byid(user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found in database.")
    return profile

def require_roles(allowed_roles: list[str]):
    def role_verifier(profile: UserEntity = Depends(get_current_user_profile)):
        if profile.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permissions to access this resource.")
        return profile
    return role_verifier

@router.get("/profile", response_model=UserEntity)
def get_profile(current_user: UserEntity = Depends(get_current_user_profile)):
    """
    Obtiene el perfil del usuario actualmente autenticado.
    Requiere cabecera: Authorization: Bearer <token>
    """
    return current_user

@router.patch("/profile", response_model=UserEntity)
def update_profile(req: UpdateProfileRequest, current_user: UserEntity = Depends(get_current_user_profile)):
    """
    Actualiza parcialmente el perfil del usuario actualmente autenticado.
    Requiere cabecera: Authorization: Bearer <token>
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
    """
    Obtiene las reservas del usuario autenticado
    """
    id_user=current_user.id
    try:
        user_reservations = user_service.get_user_reservations(id_user)
        return user_reservations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

