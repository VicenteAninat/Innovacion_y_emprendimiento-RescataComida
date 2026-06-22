from typing import List, Optional
from app.entity.ReviewsEntity import ReviewsEntity
from app.repository.ReviewsRepository import ReviewsRepository
from app.repository.ReservationsRepository import ReservationsRepository

class ReviewsService:
    def __init__(self):
        self.reviews_repository = ReviewsRepository()
        self.reservations_repository = ReservationsRepository()

    def create_review(self, user_id: str, reservation_id: int, rating: int, comment: Optional[str] = None) -> ReviewsEntity:
        # 1. Obtener la reserva con su oferta asociada
        res_data = self.reservations_repository.get_reservation_with_offer(reservation_id)
        if not res_data:
            raise ValueError("La reserva no existe.")

        # 2. Validar que la reserva pertenezca al usuario
        if res_data.get("user_id") != user_id:
            raise ValueError("No estás autorizado para calificar esta reserva.")

        # 3. Validar que la reserva esté en estado "completed"
        if res_data.get("status") != "completed":
            raise ValueError("Solo puedes evaluar reservas que estén en estado 'completed'.")

        # 4. Obtener el business_id a partir de la oferta asociada
        offer_data = res_data.get("offer")
        if not offer_data or "business_id" not in offer_data:
            raise ValueError("No se pudo obtener el comercio asociado a la oferta de esta reserva.")
        
        business_id = offer_data["business_id"]

        # 5. Crear la entidad de la reseña
        review = ReviewsEntity(
            user_id=user_id,
            business_id=business_id,
            reservation_id=reservation_id,
            rating=rating,
            comment=comment
        )
        return self.reviews_repository.create(review)

    def update_review(self, user_id: str, review_id: int, data: dict) -> Optional[ReviewsEntity]:
        # 1. Verificar si la reseña existe
        review = self.reviews_repository.get_by_id(review_id)
        if not review:
            raise ValueError("La reseña no existe.")

        # 2. Validar pertenencia de la reseña
        if review.user_id != user_id:
            raise ValueError("No estás autorizado para modificar esta reseña.")

        # 3. Actualizar
        # Limpiar datos para evitar actualizar campos no permitidos como ids
        allowed_updates = {}
        if "rating" in data:
            allowed_updates["rating"] = data["rating"]
        if "comment" in data:
            allowed_updates["comment"] = data["comment"]

        return self.reviews_repository.update(review_id, allowed_updates)

    def delete_review(self, user_id: str, review_id: int) -> bool:
        # 1. Verificar si la reseña existe
        review = self.reviews_repository.get_by_id(review_id)
        if not review:
            raise ValueError("La reseña no existe.")

        # 2. Validar pertenencia de la reseña
        if review.user_id != user_id:
            raise ValueError("No estás autorizado para eliminar esta reseña.")

        return self.reviews_repository.delete(review_id)

    def get_reviews_by_business(self, business_id: int) -> List[ReviewsEntity]:
        return self.reviews_repository.get_by_business_id(business_id)
