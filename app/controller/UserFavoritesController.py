"""User Favorites Controller.

This module provides endpoints for managing user's favorite businesses, including
adding a favorite, removing a favorite, checking favorite status, and fetching all favorites.
"""

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
    """Agrega un local comercial a la lista de favoritos del usuario autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business to add to favorites.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        UserFavoritesEntity: The user favorite mapping record created.

    Raises:
        HTTPException: If the operation fails.
    """
    try:
        return favorites_service.add_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/remove/{business_id}", response_model=bool)
def remove_favorite(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """Elimina un local comercial de la lista de favoritos del usuario autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business to remove from favorites.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        bool: True if removal was successful, False otherwise.

    Raises:
        HTTPException: If the operation fails.
    """
    try:
        return favorites_service.remove_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/{business_id}", response_model=bool)
def is_favorite(business_id: int, current_user: UserEntity = Depends(get_current_user)):
    """Verifica si el local comercial especificado está en la lista de favoritos del usuario autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business to check.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        bool: True if it is a favorite, False otherwise.

    Raises:
        HTTPException: If the operation fails.
    """
    try:
        return favorites_service.is_favorite(str(current_user.id), business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-favorites", response_model=List[BusinessesEntity])
def get_my_favorites(current_user: UserEntity = Depends(get_current_user)):
    """Obtiene todos los locales comerciales marcados como favoritos por el usuario autenticado.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[BusinessesEntity]: List of favorite businesses.

    Raises:
        HTTPException: If the operation fails.
    """
    try:
        return favorites_service.get_favorites_by_user(str(current_user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
