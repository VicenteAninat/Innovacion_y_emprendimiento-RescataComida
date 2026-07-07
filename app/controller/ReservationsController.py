"""Reservations Controller.

This module handles routes and request schemas for reservations on offers, including
creating, listing personal and system-wide reservations, partial updates, and deletion.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.service.ReservationsService import ReservationsService
from app.entity.ReservationsEntity import ReservationsEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user, get_current_user_profile

router = APIRouter(prefix="/reservations", tags=["Reservations"])
reservations_service = ReservationsService()

class ReservationCreateRequest(BaseModel):
    """Request schema for creating a new reservation.

    Attributes:
        offer_id (int): Unique identifier of the target offer.
        quantity (int): Number of bags/units to reserve. Defaults to 1.
        payment_method (Optional[str]): Method of payment chosen (e.g. credit_card).
        transaction_fee (Optional[float]): Optional fee for processing transaction.
    """
    offer_id: int
    quantity: int = 1
    payment_method: Optional[str] = None
    transaction_fee: Optional[float] = None

@router.post("/create", response_model=ReservationsEntity)
def create_reservation(
    data: ReservationCreateRequest,
    current_user: UserEntity = Depends(get_current_user)
):
    """Crea una reserva en estado 'pending' para una oferta.

    El trigger de PostgreSQL verifica que haya stock y lo descuenta.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        data (ReservationCreateRequest): Details of the reservation to create.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        ReservationsEntity: The created reservation entity.

    Raises:
        HTTPException: If creation fails or validation fails.
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
    """Obtiene las reservas asociadas al usuario autenticado actual.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): Authenticated user payload.

    Returns:
        List[ReservationsEntity]: A list of reservations belonging to the user.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return reservations_service.get_reservations_by_user_id(str(current_user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ReservationUpdateRequest(BaseModel):
    """Request schema for updating an existing reservation.

    Attributes:
        quantity (Optional[int]): Number of units reserved.
        status (Optional[str]): Updated status of reservation (e.g. completed, cancelled).
        payment_method (Optional[str]): Method of payment.
        transaction_fee (Optional[float]): Processing fee.
    """
    quantity: Optional[int] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_fee: Optional[float] = None

@router.get("/get_all", response_model=List[ReservationsEntity])
def get_all_reservations(current_user: UserEntity = Depends(get_current_user)):
    """Lista todas las reservas del sistema (Ruta administrativa/consulta).

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): Authenticated user payload.

    Returns:
        List[ReservationsEntity]: A list of all reservations in the system.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return reservations_service.get_all_reservations()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{id_val}", response_model=ReservationsEntity)
def get_reservation_by_id(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """Obtiene el detalle de una reserva específica por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the reservation to fetch.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        ReservationsEntity: The requested reservation.

    Raises:
        HTTPException: If reservation is not found or retrieval fails.
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
    """Actualiza parcialmente los datos de una reserva por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the reservation to update.
        data (ReservationUpdateRequest): Fields to update.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        ReservationsEntity: The updated reservation entity.

    Raises:
        HTTPException: If the update fails.
    """
    try:
        return reservations_service.update_reservation(id_val, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{id_val}", response_model=bool)
def delete_reservation(id_val: int, current_user: UserEntity = Depends(get_current_user)):
    """Elimina físicamente una reserva por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the reservation to delete.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        bool: True if deletion was successful, False otherwise.

    Raises:
        HTTPException: If deletion fails.
    """
    try:
        return reservations_service.delete_reservation(id_val)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel/{id_val}", response_model=ReservationsEntity)
def cancel_reservation(id_val: int, current_user: UserEntity = Depends(get_current_user_profile)):
    """Cancela una reserva existente y devuelve su stock a la oferta.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the reservation to cancel.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        ReservationsEntity: The cancelled reservation entity.

    Raises:
        HTTPException: If cancellation fails (400) or internal error occurs (500).
    """
    try:
        return reservations_service.cancel_reservation(
            id_val=id_val,
            user_id=str(current_user.id),
            user_role=current_user.role
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/pay/{id_val}", response_model=ReservationsEntity)
def pay_reservation(id_val: int, current_user: UserEntity = Depends(get_current_user_profile)):
    """Registra el pago de una reserva y cambia su estado a 'paid'.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        id_val (int): ID of the reservation to pay.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        ReservationsEntity: The paid reservation entity.

    Raises:
        HTTPException: If payment fails (400) or internal error occurs (500).
    """
    try:
        return reservations_service.pay_reservation(
            id_val=id_val,
            user_id=str(current_user.id)
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
