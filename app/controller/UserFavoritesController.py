from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.service.UserFavoritesService import UserFavoritesService
from app.entity.UserFavoritesEntity import UserFavoritesEntity
from app.entity.BusinessesEntity import BusinessesEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/favorites", tags=["UserFavorites"])
favorites_service = UserFavoritesService()

@router.post("/add/{business_id}", response_model=UserFavoritesEntity)
def add_favorite(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Agrega un local comercial a la lista de favoritos del usuario autenticado.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return favorites_service.add_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/remove/{business_id}", response_model=bool)
def remove_favorite(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Elimina un local comercial de la lista de favoritos del usuario autenticado.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return favorites_service.remove_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/{business_id}", response_model=bool)
def is_favorite(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """
    Verifica si el local comercial especificado está en la lista de favoritos del usuario autenticado.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return favorites_service.is_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-favorites", response_model=List[BusinessesEntity])
def get_my_favorites(current_user: UserEntity = Depends(get_current_user)):
    """
    Obtiene todos los locales comerciales marcados como favoritos por el usuario autenticado.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return favorites_service.get_favorites_by_user(str(current_user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
