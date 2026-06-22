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
    reservation_id: int
    rating: int = Field(..., ge=1, le=5, description="Calificación entre 1 y 5 estrellas")
    comment: Optional[str] = None

class ReviewUpdateRequest(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Calificación entre 1 y 5 estrellas")
    comment: Optional[str] = None

@router.post("/create", response_model=ReviewsEntity)
def create_review(
    data: ReviewCreateRequest,
    current_user: UserEntity = Depends(get_current_user)
):
    """
    Crea una reseña y calificación asociada a una reserva.
    La reserva debe estar completada y pertenecer al usuario.
    Requiere cabecera: Authorization: Bearer <token>
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
    """
    Actualiza el comentario o la calificación de una reseña existente.
    El usuario debe ser el propietario de la reseña.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        # Convertimos la información a dict excluyendo los campos indefinidos
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
    """
    Elimina físicamente una reseña del sistema.
    El usuario debe ser el propietario de la reseña.
    Requiere cabecera: Authorization: Bearer <token>
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
    """
    Obtiene todas las reseñas y calificaciones de un comercio específico.
    Requiere cabecera: Authorization: Bearer <token>
    """
    try:
        return reviews_service.get_reviews_by_business(business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
