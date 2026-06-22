from typing import List, Optional
from app.entity.ReservationsEntity import ReservationsEntity
from app.config.supabase_client import supabase
from .BaseRepository import BaseRepository

class ReservationsRepository(BaseRepository[ReservationsEntity]):
    def __init__(self):
        super().__init__(ReservationsEntity, "reservations")

    def get_by_user_id(self, user_id: str) -> List[ReservationsEntity]:
        # Carga la reserva e incluye los datos de la oferta asociada
        response = (
            supabase.table(self.table_name)
            .select("*, offer(*)")
            .eq("user_id", user_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_by_business_id(self, business_id: int) -> List[ReservationsEntity]:
        # Obtiene las reservas buscando a través del business_id de la oferta
        response = (
            supabase.table(self.table_name)
            .select("*, offer!inner(*)")
            .eq("offer.business_id", business_id)
            .execute()
        )
        return [self.model_class(**item) for item in response.data]

    def get_reservation_with_offer(self, id_val: int) -> Optional[dict]:
        response = (
            supabase.table(self.table_name)
            .select("*, offer(*)")
            .eq("id", id_val)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]
