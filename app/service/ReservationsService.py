"""Reservations Service.

This module defines the ReservationsService class which contains the business logic for creating and managing reservations.
"""

from typing import List, Optional
from app.repository.ReservationsRepository import ReservationsRepository
from app.entity.ReservationsEntity import ReservationsEntity
from app.repository.OffersRepository import OffersRepository

class ReservationsService:
    """Service class encapsulating reservation validation and processing logic."""

    def __init__(self):
        """Initializes the service by setting up repositories for reservations and offers."""
        self.reservations_repository = ReservationsRepository()
        self.offers_repository = OffersRepository()

    def get_reservations_by_user_id(self, user_id: str) -> List[ReservationsEntity]:
        """Retrieves all reservations associated with a specific user.

        Args:
            user_id (str): UUID string of the customer.

        Returns:
            List[ReservationsEntity]: List of reservations, or empty list if none found.
        """
        reservas = self.reservations_repository.get_by_user_id(user_id)
        if not reservas:
            return []     
        return reservas

    def create_reservation(self, reservation: ReservationsEntity) -> ReservationsEntity:
        """Validates stock, calculates the total price, and creates a reservation.

        Args:
            reservation (ReservationsEntity): The temporary reservation data.

        Returns:
            ReservationsEntity: The created reservation record from the database.

        Raises:
            ValueError: If the offer does not exist, is inactive, or has insufficient stock.
        """
        # 1. Obtener la oferta
        offer = self.offers_repository.get_by_id(reservation.offer_id, "id")
        if not offer:
            raise ValueError("La oferta seleccionada no existe.")
        
        # 2. Validar que la oferta esté activa
        if offer.status != "active":
            raise ValueError("La oferta seleccionada no está disponible.")

        # Verificar si la oferta ha expirado en su horario de retiro
        from datetime import datetime, timezone
        if offer.pickup_end_time:
            now = datetime.now(offer.pickup_end_time.tzinfo) if offer.pickup_end_time.tzinfo else datetime.utcnow()
            if now > offer.pickup_end_time:
                raise ValueError("El horario de retiro para esta oferta ya ha expirado.")

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
        """Retrieves all reservations in the system.

        Returns:
            List[ReservationsEntity]: List of all reservations.
        """
        return self.reservations_repository.get_all()

    def get_reservation_by_id(self, id_val: int) -> Optional[ReservationsEntity]:
        """Fetches a reservation by its ID.

        Args:
            id_val (int): ID of the reservation.

        Returns:
            Optional[ReservationsEntity]: The reservation entity if found, otherwise None.
        """
        return self.reservations_repository.get_by_id(id_val)

    def update_reservation(self, id_val: int, data: dict) -> Optional[ReservationsEntity]:
        """Updates attributes of a reservation.

        Args:
            id_val (int): ID of the reservation to update.
            data (dict): Dict of fields to update.

        Returns:
            Optional[ReservationsEntity]: The updated reservation entity if found, otherwise None.
        """
        return self.reservations_repository.update(id_val, data)

    def delete_reservation(self, id_val: int) -> bool:
        """Deletes a reservation from the system.

        Args:
            id_val (int): ID of the reservation to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        return self.reservations_repository.delete(id_val)

    def cancel_reservation(self, id_val: int, user_id: str, user_role: str) -> ReservationsEntity:
        """Cancels a reservation and returns its stock to the offer.

        Args:
            id_val (int): Unique reservation ID.
            user_id (str): UUID string of the requesting user.
            user_role (str): Role of the requesting user ('customer', 'worker', 'admin').

        Returns:
            ReservationsEntity: The updated reservation details.

        Raises:
            ValueError: If the reservation does not exist, status is already cancelled or collected,
                        or the user does not have permission.
        """
        reservation = self.get_reservation_by_id(id_val)
        if not reservation:
            raise ValueError("La reserva no existe.")
            
        # Validar permisos
        if user_role != "admin" and reservation.user_id != user_id:
            raise ValueError("No tienes permiso para cancelar esta reserva.")
            
        # Validar estado
        if reservation.status == "cancelled":
            raise ValueError("La reserva ya está cancelada.")
        if reservation.status == "collected":
            raise ValueError("No se puede cancelar una reserva que ya ha sido retirada.")
            
        # Actualizar estado a 'cancelled'
        updated = self.update_reservation(id_val, {"status": "cancelled"})
        if not updated:
            raise ValueError("No se pudo actualizar el estado de la reserva.")
        return updated

    def pay_reservation(self, id_val: int, user_id: str) -> ReservationsEntity:
        """Registers payment for a reservation and changes its status to 'paid'.

        Args:
            id_val (int): Unique reservation ID.
            user_id (str): UUID string of the customer paying.

        Returns:
            ReservationsEntity: The updated reservation details.

        Raises:
            ValueError: If the reservation doesn't exist, is not owned by the user, is already paid,
                        is cancelled, is collected, or if payment timed out (exceeded 15 minutes).
        """
        reservation = self.get_reservation_by_id(id_val)
        if not reservation:
            raise ValueError("La reserva no existe.")
            
        # Validar pertenencia
        if reservation.user_id != user_id:
            raise ValueError("No tienes permiso para pagar esta reserva.")
            
        # Validar si ya está pagada
        if reservation.status == "paid":
            raise ValueError("La reserva ya ha sido pagada.")
            
        # Validar si está cancelada
        if reservation.status == "cancelled":
            raise ValueError("La reserva está cancelada y no se puede pagar.")
            
        # Validar si ya fue retirada
        if reservation.status == "collected":
            raise ValueError("No se puede pagar una reserva que ya ha sido retirada.")
            
        # Validar límite de tiempo de 15 minutos (900 segundos)
        from datetime import datetime
        if reservation.created_at:
            delta = datetime.now(reservation.created_at.tzinfo) - reservation.created_at
            if delta.total_seconds() > 900:  # 15 minutos
                # Cancelar automáticamente
                self.update_reservation(id_val, {"status": "cancelled"})
                raise ValueError("El tiempo límite de 15 minutos para pagar ha expirado. La reserva ha sido cancelada.")
                
        # Actualizar estado a 'paid'
        updated = self.update_reservation(id_val, {"status": "paid"})
        if not updated:
            raise ValueError("No se pudo registrar el pago de la reserva.")
        return updated
