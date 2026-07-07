"""Food Banks Controller.

This module provides endpoints for managing food bank organizations, including
registration, details retrieval, partial updates, and deletion.
"""

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
    """Request schema for creating a new food bank.

    Attributes:
        rut (str): Unique RUT (tax identifier) of the food bank.
        name (Optional[str]): Name of the food bank organization.
        contact_email (Optional[str]): Contact email address.
        contact_phone (Optional[str]): Contact phone number.
        address (Optional[str]): Physical address of the food bank.
    """
    rut: str
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

class FoodBankUpdateRequest(BaseModel):
    """Request schema for updating an existing food bank.

    Attributes:
        rut (Optional[str]): Unique RUT (tax identifier) of the food bank.
        name (Optional[str]): Name of the food bank organization.
        contact_email (Optional[str]): Contact email address.
        contact_phone (Optional[str]): Contact phone number.
        address (Optional[str]): Physical address of the food bank.
    """
    rut: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

@router.post("/create", response_model=FoodBanksEntity)
def create_food_bank(data: FoodBankCreateRequest, current_user: UserEntity = Depends(get_current_user)):
    """Registra una nueva organización o banco de alimentos en el sistema.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        data (FoodBankCreateRequest): Food bank creation parameters.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        FoodBanksEntity: The registered food bank.

    Raises:
        HTTPException: If creation fails.
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
    """Obtiene el listado completo de todos los bancos de alimentos registrados.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): Authenticated user payload.

    Returns:
        List[FoodBanksEntity]: List of all registered food banks.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return food_banks_service.get_all_food_banks()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{id_val}", response_model=FoodBanksEntity)
def get_food_bank_by_id(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """Obtiene los detalles de un banco de alimentos específico por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the food bank to fetch.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        FoodBanksEntity: The requested food bank.

    Raises:
        HTTPException: If food bank is not found or retrieval fails.
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
    """Actualiza parcialmente la información de un banco de alimentos por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the food bank to update.
        data (FoodBankUpdateRequest): Fields to update.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        FoodBanksEntity: The updated food bank object.

    Raises:
        HTTPException: If the update fails.
    """
    try:
        return food_banks_service.update_food_bank(id_val, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{id_val}", response_model=bool)
def delete_food_bank(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """Elimina físicamente un banco de alimentos por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the food bank to delete.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        bool: True if deletion was successful, False otherwise.

    Raises:
        HTTPException: If deletion fails.
    """
    try:
        return food_banks_service.delete_food_bank(id_val)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
