from app.repository.BusinessesRepository import BusinessesRepository
from app.entity.BusinessesEntity import BusinessesEntity
from typing import Optional, List
class BusinessesService:
    def __init__(self):
        self.businesses_repository = BusinessesRepository()

    def get_all_businesses(self) -> List[BusinessesEntity]:
        return self.businesses_repository.get_all()
    
    def get_business_by_id(self, business_id: int) -> Optional[BusinessesEntity]:
        return self.businesses_repository.get_by_id(business_id)
    
    def create_businesses(self,  rut: str, name:str, category:str, address: str, location:str ) -> Optional[BusinessesEntity]:
        business=BusinessesEntity(
            rut=rut,
            name=name,
            category=  category,
            address = address,
            location= location,
            is_premium= False
        )
        return self.businesses_repository.create(business)
    
    def update_businesses(self, business_id: str, data: dict) -> Optional[BusinessesEntity]:
        return self.businesses_repository.update(business_id,data,"id")
    
    def delete_businesses(self,business_id: str) -> Optional[int] :
        return self.businesses_repository.delete(business_id,"id")
    
    def get_nearby_businesses_with_active_offers(self, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        return self.businesses_repository.get_nearby_businesses_with_active_offers(lat, lng, radius_km)

    def get_favorite_businesses_with_active_offers_nearby(self, user_id: str, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        return self.businesses_repository.get_favorite_businesses_with_active_offers_nearby(user_id, lat, lng, radius_km)