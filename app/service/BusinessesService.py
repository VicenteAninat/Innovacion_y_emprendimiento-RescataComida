"""Businesses Service.

This module defines the BusinessesService class which manages business operations logic.
"""

from app.repository.BusinessesRepository import BusinessesRepository
from app.entity.BusinessesEntity import BusinessesEntity
from typing import Optional, List

class BusinessesService:
    """Service class encapsulating business operational logic."""

    def __init__(self):
        """Initializes the service by setting up the BusinessesRepository."""
        self.businesses_repository = BusinessesRepository()

    def get_all_businesses(self) -> List[BusinessesEntity]:
        """Retrieves a list of all businesses registered in the system.

        Returns:
            List[BusinessesEntity]: All registered business entities.
        """
        return self.businesses_repository.get_all()
    
    def get_business_by_id(self, business_id: int) -> Optional[BusinessesEntity]:
        """Fetches a business details using its ID.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            Optional[BusinessesEntity]: The business entity if found, otherwise None.
        """
        return self.businesses_repository.get_by_id(business_id)
    
    def create_businesses(self, rut: str, name: str, category: str, address: str, location: str) -> Optional[BusinessesEntity]:
        """Creates a new business in the system.

        Args:
            rut (str): Tax identification number/RUT.
            name (str): Commercial name of the business.
            category (str): Category/type of industry.
            address (str): Physical address.
            location (str): Geographical location representation.

        Returns:
            Optional[BusinessesEntity]: The newly created business entity.
        """
        business = BusinessesEntity(
            rut=rut,
            name=name,
            category=category,
            address=address,
            location=location,
            is_premium=False
        )
        return self.businesses_repository.create(business)
    
    def update_businesses(self, business_id: str, data: dict) -> Optional[BusinessesEntity]:
        """Partially updates business attributes.

        Args:
            business_id (str): ID of the business to update.
            data (dict): Dictionary containing fields to modify.

        Returns:
            Optional[BusinessesEntity]: The updated business entity if found, otherwise None.
        """
        return self.businesses_repository.update(business_id, data, "id")
    
    def delete_businesses(self, business_id: str) -> Optional[int]:
        """Deletes a business from the database.

        Args:
            business_id (str): ID of the business to delete.

        Returns:
            Optional[int]: Number of affected rows (usually 1 on success).
        """
        return self.businesses_repository.delete(business_id, "id")
    
    def get_nearby_businesses_with_active_offers(self, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        """Finds businesses in range that currently have active offers.

        Args:
            lat (float): Latitude coordinate.
            lng (float): Longitude coordinate.
            radius_km (float): Search radius in kilometers. Defaults to 5.0.

        Returns:
            List[BusinessesEntity]: Nearby businesses with active offers.
        """
        return self.businesses_repository.get_nearby_businesses_with_active_offers(lat, lng, radius_km)

    def get_favorite_businesses_with_active_offers_nearby(self, user_id: str, lat: float, lng: float, radius_km: float = 5.0) -> List[BusinessesEntity]:
        """Finds favorite businesses in range that currently have active offers.

        Args:
            user_id (str): UUID string of the customer.
            lat (float): Latitude coordinate.
            lng (float): Longitude coordinate.
            radius_km (float): Search radius in kilometers. Defaults to 5.0.

        Returns:
            List[BusinessesEntity]: Nearby favorite businesses with active offers.
        """
        return self.businesses_repository.get_favorite_businesses_with_active_offers_nearby(user_id, lat, lng, radius_km)
