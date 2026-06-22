from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.service.BusinessesService import BusinessesService
from app.entity.BusinessesEntity import BusinessesEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/businesses", tags=["Businesses"])
business_service = BusinessesService()

class registerBusiness(BaseModel):
    rut: str
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None

@router.post("/create", response_model=BusinessesEntity)
def create_business(data: registerBusiness, current_user: UserEntity = Depends(get_current_user)):
    """
    Registra un nuevo comercio/local en la plataforma.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        new_business = business_service.create_businesses(
            data.rut,
            data.name,
            data.category,
            data.address,
            data.location
        )
        return new_business
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get_all", response_model=List[BusinessesEntity])
def get_all_business(current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene la lista completa de todos los comercios registrados.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return business_service.get_all_businesses()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get/{business_id}", response_model=BusinessesEntity)
def get_by_id(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene los detalles de un comercio específico según su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return business_service.get_business_by_id(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/update", response_model=BusinessesEntity)
def update_business(business_id: str, data: registerBusiness, current_user: UserEntity = Depends(get_current_user)):
    """
    Actualiza parcialmente los datos de un comercio.
    Recibe el business_id como parámetro de consulta (query) y los datos a actualizar en el body.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        # Convertimos el modelo Pydantic a dict excluyendo los campos que no fueron enviados
        return business_service.update_businesses(business_id, data.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{business_id}", response_model=int)
def delete_business(business_id: str, current_user: UserEntity = Depends(get_current_user)):
    """
    Elimina físicamente un comercio de la base de datos por su ID.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return business_service.delete_businesses(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nearby-with-offers", response_model=List[BusinessesEntity])
def get_nearby_with_offers(lat: float, lng: float, radius_km: float = 5.0, current_user: UserEntity = Depends(get_current_user)):
    """
    Busca los locales comerciales cercanos con ofertas activas utilizando PostGIS.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return business_service.get_nearby_businesses_with_active_offers(lat, lng, radius_km)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/favorite-nearby", response_model=List[BusinessesEntity])
def get_favorite_nearby_businesses(
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    current_user: UserEntity = Depends(get_current_user)
):
    """
    Busca los locales comerciales favoritos del usuario que tengan ofertas activas y estén en el rango.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return business_service.get_favorite_businesses_with_active_offers_nearby(
            str(current_user.id), lat, lng, radius_km
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
