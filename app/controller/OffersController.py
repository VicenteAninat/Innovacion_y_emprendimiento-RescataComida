"""Offers Controller.

This module provides endpoints for creating, retrieving, updating, and deleting
discounted food offer bags, along with querying options (like nearby favorite business offers).
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.service.OffersService import OffersService
from app.entity.OffersEntity import OffersEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user, get_current_user_profile, require_roles

router = APIRouter(prefix="/offers", tags=["Offers"])
offers_service = OffersService()

# Schemas de validación para las peticiones de ofertas
class CreateOfferRequest(BaseModel):
    """Request schema for creating a new food offer.

    Attributes:
        business_id (int): Unique identifier of the associated business.
        title (str): Title of the surprise bag / offer.
        description (Optional[str]): Detailed description of what the bag might contain.
        original_price (float): Original value of the items.
        discounted_price (float): Special discounted price.
        quantity_available (Optional[int]): Number of units available. Defaults to 1.
        pickup_start_time (datetime): Start time window for picking up the items.
        pickup_end_time (datetime): End time window for picking up the items.
        status (Optional[str]): Status of the offer. Defaults to "active".
        kg_saved_per_unit (Optional[float]): Estimated kilograms of food saved per unit.
        co2_avoided_per_unit (Optional[float]): Estimated carbon dioxide emissions avoided per unit.
    """
    business_id: int
    title: str
    description: Optional[str] = None
    original_price: float
    discounted_price: float
    quantity_available: Optional[int] = 1
    pickup_start_time: datetime
    pickup_end_time: datetime
    status: Optional[str] = "active"
    kg_saved_per_unit: Optional[float] = None
    co2_avoided_per_unit: Optional[float] = None

class UpdateOfferRequest(BaseModel):
    """Request schema for updating an existing food offer.

    Attributes:
        title (Optional[str]): Title of the surprise bag / offer.
        description (Optional[str]): Detailed description of the offer.
        original_price (Optional[float]): Original value of the items.
        discounted_price (Optional[float]): Special discounted price.
        quantity_available (Optional[int]): Number of units available.
        pickup_start_time (Optional[datetime]): Start time window for pickup.
        pickup_end_time (Optional[datetime]): End time window for pickup.
        status (Optional[str]): Status of the offer.
        kg_saved_per_unit (Optional[float]): Kilograms of food saved per unit.
        co2_avoided_per_unit (Optional[float]): Carbon dioxide avoided per unit.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    original_price: Optional[float] = None
    discounted_price: Optional[float] = None
    quantity_available: Optional[int] = None
    pickup_start_time: Optional[datetime] = None
    pickup_end_time: Optional[datetime] = None
    status: Optional[str] = None
    kg_saved_per_unit: Optional[float] = None
    co2_avoided_per_unit: Optional[float] = None

# --- Operaciones CRUD ---

@router.post("/create", response_model=OffersEntity)
def create_offer(
    req: CreateOfferRequest,
    current_user: UserEntity = Depends(require_roles(["worker", "admin"]))
):
    """Crea y publica una nueva oferta (Bolsa Sorpresa).

    Si no se especifican, calcula automáticamente el CO2 evitado y los kg salvados.
    Los usuarios con rol 'worker' solo pueden crear ofertas para su propio negocio.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        req (CreateOfferRequest): Detailed data for creating the offer.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        OffersEntity: The created offer details.

    Raises:
        HTTPException: If roles are unauthorized or business ownership verification fails.
    """
    try:
        # Validar permisos del worker: solo puede crear ofertas para su propio negocio
        if current_user.role == "worker" and current_user.business_id != req.business_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para crear ofertas para un comercio diferente al tuyo."
            )

        new_offer = offers_service.create_offer(
            business_id=req.business_id,
            title=req.title,
            original_price=req.original_price,
            discounted_price=req.discounted_price,
            pickup_start_time=req.pickup_start_time,
            pickup_end_time=req.pickup_end_time,
            description=req.description,
            quantity_available=req.quantity_available if req.quantity_available is not None else 1,
            status=req.status if req.status is not None else "active",
            kg_saved_per_unit=req.kg_saved_per_unit,
            co2_avoided_per_unit=req.co2_avoided_per_unit
        )
        return new_offer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all", response_model=List[OffersEntity])
def get_all_offers(current_user: UserEntity = Depends(get_current_user)):
    """Obtiene la lista completa de todas las ofertas registradas en la base de datos.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): Authenticated user payload.

    Returns:
        List[OffersEntity]: A list of all offers.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return offers_service.get_all_offers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{offer_id}", response_model=OffersEntity)
def get_by_id(offer_id: int, current_user: UserEntity = Depends(get_current_user)):
    """Obtiene el detalle de una oferta específica por su ID.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        offer_id (int): ID of the offer.
        current_user (UserEntity): Authenticated user payload.

    Returns:
        OffersEntity: Details of the specified offer.

    Raises:
        HTTPException: If the offer is not found.
    """
    try:
        offer = offers_service.get_offer_by_id(offer_id)
        if not offer:
            raise HTTPException(status_code=404, detail="Oferta no encontrada.")
        return offer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{offer_id}", response_model=OffersEntity)
def update_offer(
    offer_id: int,
    req: UpdateOfferRequest,
    current_user: UserEntity = Depends(require_roles(["worker", "admin"]))
):
    """Actualiza parcialmente una oferta existente.

    Recalcula automáticamente el CO2 evitado y los kg salvados si el precio original o peso cambian.
    Los usuarios con rol 'worker' solo pueden modificar ofertas de su propio negocio.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        offer_id (int): ID of the offer to update.
        req (UpdateOfferRequest): Partial fields to update.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        OffersEntity: The updated offer entity.

    Raises:
        HTTPException: If the offer is not found or authorization check fails.
    """
    try:
        # Obtener oferta existente para verificar pertenencia
        existing_offer = offers_service.get_offer_by_id(offer_id)
        if not existing_offer:
            raise HTTPException(status_code=404, detail="Oferta no encontrada.")
        
        # Validar permisos del worker
        if current_user.role == "worker" and current_user.business_id != existing_offer.business_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para modificar ofertas de este comercio."
            )

        update_data = req.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar.")

        # Recalcular kg_saved_per_unit y co2_avoided_per_unit si se modificó el precio original o los kg
        if "original_price" in update_data:
            orig_price = update_data["original_price"]
            if "kg_saved_per_unit" not in update_data:
                update_data["kg_saved_per_unit"] = round(orig_price / 5000.0, 2) if orig_price > 0 else 1.0
            if "co2_avoided_per_unit" not in update_data:
                update_data["co2_avoided_per_unit"] = round(update_data["kg_saved_per_unit"] * 2.5, 2)
        elif "kg_saved_per_unit" in update_data and "co2_avoided_per_unit" not in update_data:
            update_data["co2_avoided_per_unit"] = round(update_data["kg_saved_per_unit"] * 2.5, 2)

        updated_offer = offers_service.update_offer(offer_id, update_data)
        if not updated_offer:
            raise HTTPException(status_code=404, detail="No se pudo actualizar la oferta.")
        return updated_offer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete/{offer_id}", response_model=bool)
def delete_offer(
    offer_id: int,
    current_user: UserEntity = Depends(require_roles(["worker", "admin"]))
):
    """Elimina físicamente una oferta del sistema por su ID.

    Los usuarios con rol 'worker' solo pueden eliminar ofertas de su propio negocio.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        offer_id (int): ID of the offer to delete.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If the offer is not found or authorization fails.
    """
    try:
        # Obtener oferta existente para verificar pertenencia
        existing_offer = offers_service.get_offer_by_id(offer_id)
        if not existing_offer:
            raise HTTPException(status_code=404, detail="Oferta no encontrada.")
        
        # Validar permisos del worker
        if current_user.role == "worker" and current_user.business_id != existing_offer.business_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para eliminar ofertas de este comercio."
            )

        success = offers_service.delete_offer(offer_id)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo eliminar la oferta.")
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/business/{business_id}", response_model=List[OffersEntity])
def get_by_business(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """Obtiene todas las ofertas registradas de un negocio específico (incluye inactivas).

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[OffersEntity]: List of offers associated with the business.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return offers_service.offers_by_business(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Consultas de Negocio Existentes ---

@router.get("/favorite-nearby", response_model=List[OffersEntity])
def get_favorite_nearby_offers(
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    current_user: UserEntity = Depends(get_current_user)
):
    """Obtiene las ofertas activas de los comercios favoritos dentro de un radio geográfico (PostGIS).

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        lat (float): Latitude coordinate.
        lng (float): Longitude coordinate.
        radius_km (float): Search radius in kilometers. Defaults to 5.0.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[OffersEntity]: A list of active offers from favorite businesses.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return offers_service.get_favorite_businesses_offers_nearby(
            str(current_user.id), lat, lng, radius_km
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/active", response_model=List[OffersEntity])
def get_global_active_offers(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: float = 5.0,
    limit: int = 10,
    offset: int = 0,
    current_user: UserEntity = Depends(get_current_user)
):
    """Obtiene el feed global de ofertas activas y con stock disponible.

    Soporta geolocalización opcional (ordenando por distancia si se envían lat y lng) y paginación.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        lat (Optional[float]): Latitude coordinate.
        lng (Optional[float]): Longitude coordinate.
        radius_km (float): Search radius in kilometers. Defaults to 5.0.
        limit (int): Limit of results. Defaults to 10.
        offset (int): Offset of results. Defaults to 0.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[OffersEntity]: A list of active offers.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return offers_service.get_active_offers(lat, lng, radius_km, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/active/{business_id}", response_model=List[OffersEntity])
def get_active_offers(
    business_id: int,
    current_user: UserEntity = Depends(get_current_user)
):
    """Obtiene únicamente las ofertas activas con stock disponible de un negocio en particular.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[OffersEntity]: List of active offers with positive stock.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return offers_service.get_active_offers_by_business(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
