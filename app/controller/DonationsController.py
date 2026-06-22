from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.service.DonationsService import DonationsService
from app.entity.DonationsEntity import DonationsEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/donations", tags=["Donations"])
donations_service = DonationsService()

class DonationCreateRequest(BaseModel):
    business_id: int
    food_bank_id: int
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    tax_deductible_receipt_url: Optional[str] = None

class DonationUpdateRequest(BaseModel):
    business_id: Optional[int] = None
    food_bank_id: Optional[int] = None
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    tax_deductible_receipt_url: Optional[str] = None

@router.post("/create", response_model=DonationsEntity)
def create_donation(data: DonationCreateRequest, current_user: UserEntity = Depends(get_current_user)):
    """
    Registra un envío de excedentes/donación de un local comercial a un banco de alimentos.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return donations_service.create_donation(
            business_id=data.business_id,
            food_bank_id=data.food_bank_id,
            description=data.description,
            weight_kg=data.weight_kg,
            tax_deductible_receipt_url=data.tax_deductible_receipt_url
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all", response_model=List[DonationsEntity])
def get_all_donations(current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene el listado completo e historial de todas las donaciones registradas en el sistema.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return donations_service.get_all_donations()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{id_val}", response_model=DonationsEntity)
def get_donation_by_id(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene los detalles de una donación específica por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        donation = donations_service.get_donation_by_id(id_val)
        if not donation:
            raise HTTPException(status_code=404, detail="Donación no encontrada")
        return donation
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/business/{business_id}", response_model=List[DonationsEntity])
def get_donations_by_business(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Recupera el historial completo de donaciones realizadas por un comercio específico.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return donations_service.get_donations_by_business(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{id_val}", response_model=DonationsEntity)
def update_donation(id_val: int, data: DonationUpdateRequest, current_user: UserEntity = Depends(get_current_user)):
    """
    Actualiza parcialmente los datos de un registro de donación.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return donations_service.update_donation(id_val, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{id_val}", response_model=bool)
def delete_donation(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Elimina físicamente un registro de donación del sistema.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return donations_service.delete_donation(id_val)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
