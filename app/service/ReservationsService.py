from typing import List, Optional
from app.repository.ReservationsRepository import ReservationsRepository
from app.entity.ReservationsEntity import ReservationsEntity
from app.repository.OffersRepository import OffersRepository

class ReservationsService:
    def __init__(self):
        self.reservations_repository = ReservationsRepository()
        self.offers_repository = OffersRepository()
    def get_reservations_by_user_id(self, user_id: str):
        reservas = self.reservations_repository.get_by_user_id(user_id)
        if not reservas:
            return []     
        return reservas
    def create_reservation(self, reservation):
        # 1. Obtener la oferta
        offer = self.offers_repository.get_by_id(reservation.offer_id, "id")
        if not offer:
            raise ValueError("La oferta seleccionada no existe.")
        
        # 2. Validar que la oferta esté activa
        if offer.status != "active":
            raise ValueError("La oferta seleccionada no está disponible.")

        # 3. Preparar los datos de la reserva
        reservation_data = reservation.dict() if hasattr(reservation, "dict") else dict(reservation)
        reservation_data["total_price"] = reservation.quantity * offer.discounted_price
        reservation_data["status"] = "pending"
        # Crear la entidad de reserva
        reservation_entity = ReservationsEntity(**reservation_data)

        # 4. Crear reserva (El trigger en PostgreSQL se encargará de validar stock y descontarlo)
        try:
            return self.reservations_repository.create(reservation_entity)
        except Exception as e:
            error_msg = str(e)
            if "Stock insuficiente" in error_msg:
                raise ValueError("No hay suficiente stock disponible para la oferta seleccionada.")
            raise ValueError(f"No se pudo crear la reserva: {error_msg}")

    def get_all_reservations(self) -> List[ReservationsEntity]:
        return self.reservations_repository.get_all()

    def get_reservation_by_id(self, id_val: int) -> Optional[ReservationsEntity]:
        return self.reservations_repository.get_by_id(id_val)

    def update_reservation(self, id_val: int, data: dict) -> Optional[ReservationsEntity]:
        return self.reservations_repository.update(id_val, data)

    def delete_reservation(self, id_val: int) -> bool:
        return self.reservations_repository.delete(id_val)

        
        
