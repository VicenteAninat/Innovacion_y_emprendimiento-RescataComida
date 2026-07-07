"""Reviews Controller.

This module provides endpoints for creating, updating, deleting, and fetching
reviews/ratings for completed reservations of local business offers.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from app.service.ReviewsService import ReviewsService
from app.entity.ReviewsEntity import ReviewsEntity
from app.entity.UserEntity import UserEntity
from app.controller.AuthController import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])
reviews_service = ReviewsService()

class ReviewCreateRequest(BaseModel):
    """Request schema for creating a review.

    Attributes:
        reservation_id (int): ID of the completed reservation being reviewed.
        rating (int): Star rating given, from 1 to 5.
        comment (Optional[str]): Text review comment.
    """
    reservation_id: int
    rating: int = Field(..., ge=1, le=5, description="Calificación entre 1 y 5 estrellas")
    comment: Optional[str] = None

class ReviewUpdateRequest(BaseModel):
    """Request schema for updating a review.

    Attributes:
        rating (Optional[int]): Updated star rating, from 1 to 5.
        comment (Optional[str]): Updated text review comment.
    """
    rating: Optional[int] = Field(None, ge=1, le=5, description="Calificación entre 1 y 5 estrellas")
    comment: Optional[str] = None

@router.post("/create", response_model=ReviewsEntity)
def create_review(
    data: ReviewCreateRequest,
    current_user: UserEntity = Depends(get_current_user)
):
    """Crea una reseña y calificación asociada a una reserva.

    La reserva debe estar completada y pertenecer al usuario.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        data (ReviewCreateRequest): Information for the review.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        ReviewsEntity: The created review.

    Raises:
        HTTPException: If the creation fails or inputs are invalid.
    """
    try:
        return reviews_service.create_review(
            user_id=str(current_user.id),
            reservation_id=data.reservation_id,
            rating=data.rating,
            comment=data.comment
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.patch("/update/{review_id}", response_model=ReviewsEntity)
def update_review(
    review_id: int,
    data: ReviewUpdateRequest,
    current_user: UserEntity = Depends(get_current_user)
):
    """Actualiza el comentario o la calificación de una reseña existente.

    El usuario debe ser el propietario de la reseña.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        review_id (int): ID of the review to update.
        data (ReviewUpdateRequest): Fields to update.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        ReviewsEntity: The updated review.

    Raises:
        HTTPException: If the review is not found, unauthorized, or update fails.
    """
    try:
        updated_review = reviews_service.update_review(
            user_id=str(current_user.id),
            review_id=review_id,
            data=data.dict(exclude_unset=True)
        )
        return updated_review
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.delete("/delete/{review_id}", response_model=bool)
def delete_review(
    review_id: int,
    current_user: UserEntity = Depends(get_current_user)
):
    """Elimina físicamente una reseña del sistema.

    El usuario debe ser el propietario de la reseña.
    Requiere cabecera: Authorization: Bearer <token>

    Args:
        review_id (int): ID of the review to delete.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        bool: True if deletion was successful.

    Raises:
        HTTPException: If the review is not found, unauthorized, or deletion fails.
    """
    try:
        return reviews_service.delete_review(
            user_id=str(current_user.id),
            review_id=review_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/business/{business_id}", response_model=List[ReviewsEntity])
def get_business_reviews(
    business_id: int,
    current_user: UserEntity = Depends(get_current_user)
):
    """Obtiene todas las reseñas y calificaciones de un comercio específico.

    Requiere cabecera: Authorization: Bearer <token>

    Args:
        business_id (int): ID of the business.
        current_user (UserEntity): Authenticated user profile.

    Returns:
        List[ReviewsEntity]: List of reviews associated with the business.

    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        return reviews_service.get_reviews_by_business(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
