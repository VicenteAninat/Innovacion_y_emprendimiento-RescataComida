from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.service.FoodBanksService import FoodBanksService
from app.entity.FoodBanksEntity import FoodBanksEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/foodbanks", tags=["FoodBanks"])
food_banks_service = FoodBanksService()

class FoodBankCreateRequest(BaseModel):
    rut: str
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

class FoodBankUpdateRequest(BaseModel):
    rut: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

@router.post("/create", response_model=FoodBanksEntity)
def create_food_bank(data: FoodBankCreateRequest, current_user: UserEntity = Depends(get_current_user)):
    """
    Registra una nueva organización o banco de alimentos en el sistema.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return food_banks_service.create_food_bank(
            rut=data.rut,
            name=data.name,
            contact_email=data.contact_email,
            contact_phone=data.contact_phone,
            address=data.address
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all", response_model=List[FoodBanksEntity])
def get_all_food_banks(current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene el listado completo de todos los bancos de alimentos registrados.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return food_banks_service.get_all_food_banks()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{id_val}", response_model=FoodBanksEntity)
def get_food_bank_by_id(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene los detalles de un banco de alimentos específico por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        food_bank = food_banks_service.get_food_bank_by_id(id_val)
        if not food_bank:
            raise HTTPException(status_code=404, detail="Banco de alimentos no encontrado")
        return food_bank
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{id_val}", response_model=FoodBanksEntity)
def update_food_bank(id_val: int, data: FoodBankUpdateRequest, current_user: UserEntity = Depends(get_current_user)):
    """
    Actualiza parcialmente la información de un banco de alimentos por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return food_banks_service.update_food_bank(id_val, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{id_val}", response_model=bool)
def delete_food_bank(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Elimina físicamente un banco de alimentos por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return food_banks_service.delete_food_bank(id_val)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
