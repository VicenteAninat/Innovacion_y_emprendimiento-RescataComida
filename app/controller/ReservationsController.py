from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.service.ReservationsService import ReservationsService
from app.entity.ReservationsEntity import ReservationsEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])
reservations_service = ReservationsService()

class ReservationCreateRequest(BaseModel):
    offer_id: int
    quantity: int = 1
    payment_method: Optional[str] = None
    transaction_fee: Optional[float] = None

@router.post("/create", response_model=ReservationsEntity)
def create_reservation(
    data: ReservationCreateRequest,
    current_user: UserEntity = Depends(get_current_user)
):
    """
    Crea una reserva en estado 'pending' para una oferta.
    El trigger de PostgreSQL verifica que haya stock y lo descuenta.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        # Preparamos una entidad provisional
        # total_price se setea en 0.0 temporalmente ya que el servicio lo recalculará
        # basándose en la oferta desde la base de datos
        temp_entity = ReservationsEntity(
            user_id=str(current_user.id),
            offer_id=data.offer_id,
            quantity=data.quantity,
            total_price=0.0,
            status="pending",
            payment_method=data.payment_method,
            transaction_fee=data.transaction_fee
        )
        return reservations_service.create_reservation(temp_entity)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/my-reservations", response_model=List[ReservationsEntity])
def get_my_reservations(current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene las reservas asociadas al usuario autenticado actual.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return reservations_service.get_reservations_by_user_id(str(current_user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ReservationUpdateRequest(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_fee: Optional[float] = None

@router.get("/get_all", response_model=List[ReservationsEntity])
def get_all_reservations(current_user: UserEntity = Depends(get_current_user)):
    """
    Lista todas las reservas del sistema (Ruta administrativa/consulta).
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return reservations_service.get_all_reservations()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{id_val}", response_model=ReservationsEntity)
def get_reservation_by_id(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene el detalle de una reserva específica por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        reservation = reservations_service.get_reservation_by_id(id_val)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reservation
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{id_val}", response_model=ReservationsEntity)
def update_reservation(id_val: int, data: ReservationUpdateRequest, current_user: UserEntity = Depends(get_current_user)):
    """
    Actualiza parcialmente los datos de una reserva por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return reservations_service.update_reservation(id_val, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{id_val}", response_model=bool)
def delete_reservation(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Elimina físicamente una reserva por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return reservations_service.delete_reservation(id_val)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
