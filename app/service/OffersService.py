"""Offers Service.

This module defines the OffersService class which manages operational logic for discount offers.
"""

from typing import List, Optional
from datetime import datetime
from app.entity.OffersEntity import OffersEntity
from app.repository.OffersRepository import OffersRepository

class OffersService:
    """Service class encapsulating business logic for publishing and updating food offers."""

    def __init__(self):
        """Initializes the service by setting up the OffersRepository."""
        self.offers_repository = OffersRepository()

    def get_all_offers(self) -> List[OffersEntity]:
        """Retrieves all registered offers.

        Returns:
            List[OffersEntity]: A list of all offers.
        """
        return self.offers_repository.get_all()

    def get_offer_by_id(self, offer_id: int) -> Optional[OffersEntity]:
        """Retrieves a specific offer by ID.

        Args:
            offer_id (int): Unique identifier of the offer.

        Returns:
            Optional[OffersEntity]: The offer entity if found, otherwise None.
        """
        return self.offers_repository.get_by_id(offer_id)

    def create_offer(
        self,
        business_id: int,
        title: str,
        original_price: float,
        discounted_price: float,
        pickup_start_time: datetime,
        pickup_end_time: datetime,
        description: Optional[str] = None,
        quantity_available: int = 1,
        status: str = "active",
        kg_saved_per_unit: Optional[float] = None,
        co2_avoided_per_unit: Optional[float] = None
    ) -> OffersEntity:
        """Creates and publishes a new surprise bag offer.

        Calculates kg saved and CO2 avoided per unit based on prices if not provided.

        Args:
            business_id (int): Unique ID of the associated business.
            title (str): Title of the offer.
            original_price (float): Original retail price.
            discounted_price (float): Discounted price.
            pickup_start_time (datetime): Start time window for pickup.
            pickup_end_time (datetime): End time window for pickup.
            description (Optional[str]): Offer description.
            quantity_available (int): Quantity in stock. Defaults to 1.
            status (str): Status of the offer. Defaults to "active".
            kg_saved_per_unit (Optional[float]): Estimated kilograms of food saved.
            co2_avoided_per_unit (Optional[float]): Estimated carbon emissions avoided.

        Returns:
            OffersEntity: The newly created offer details.
        """
        # El backend calcula y asocia los kg salvados y el CO2 evitado por unidad si no se envían
        if kg_saved_per_unit is None:
            kg_saved_per_unit = round(original_price / 5000.0, 2) if original_price > 0 else 1.0

        if co2_avoided_per_unit is None:
            co2_avoided_per_unit = round(kg_saved_per_unit * 2.5, 2)

        offer = OffersEntity(
            business_id=business_id,
            title=title,
            description=description,
            original_price=original_price,
            discounted_price=discounted_price,
            quantity_available=quantity_available,
            pickup_start_time=pickup_start_time,
            pickup_end_time=pickup_end_time,
            status=status,
            kg_saved_per_unit=kg_saved_per_unit,
            co2_avoided_per_unit=co2_avoided_per_unit
        )
        return self.offers_repository.create(offer)

    def update_offer(self, offer_id: int, data: dict) -> Optional[OffersEntity]:
        """Updates attributes of an existing offer.

        Args:
            offer_id (int): ID of the offer.
            data (dict): Dict of fields to update.

        Returns:
            Optional[OffersEntity]: The updated offer entity if found, otherwise None.
        """
        return self.offers_repository.update(offer_id, data, "id")

    def delete_offer(self, offer_id: int) -> bool:
        """Deletes an offer from the system.

        Args:
            offer_id (int): ID of the offer to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        return self.offers_repository.delete(offer_id, "id")

    def offers_by_business(self, business_id: int) -> List[OffersEntity]:
        """Retrieves all offers associated with a specific business ID.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[OffersEntity]: A list of all offers for the business.
        """
        return self.offers_repository.get_offers_by_business(business_id)

    def get_active_offers_by_business(self, business_id: int) -> List[OffersEntity]:
        """Retrieves active, in-stock offers associated with a specific business ID.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[OffersEntity]: A list of active offers for the business.
        """
        return self.offers_repository.get_active_offers_by_business(business_id)

    def get_favorite_businesses_offers_nearby(
        self, user_id: str, lat: float, lng: float, radius_km: float = 5.0
    ) -> List[OffersEntity]:
        """Retrieves nearby in-stock active offers from user's favorite businesses.

        Args:
            user_id (str): UUID of the user.
            lat (float): Latitude coordinate.
            lng (float): Longitud coordinate.
            radius_km (float, optional): Search radius. Defaults to 5.0.

        Returns:
            List[OffersEntity]: List of active offers.
        """
        return self.offers_repository.get_favorite_businesses_offers_nearby(user_id, lat, lng, radius_km)

    def get_active_offers(
        self, lat: Optional[float] = None, lng: Optional[float] = None, radius_km: float = 5.0, limit: int = 10, offset: int = 0
    ) -> List[OffersEntity]:
        """Retrieves active, in-stock offers, either globally or filtered by proximity.

        Args:
            lat (Optional[float]): Latitude coordinate. Defaults to None.
            lng (Optional[float]): Longitude coordinate. Defaults to None.
            radius_km (float): Max search radius in km. Defaults to 5.0.
            limit (int): Maximum records to retrieve. Defaults to 10.
            offset (int): Starting index offset. Defaults to 0.

        Returns:
            List[OffersEntity]: List of active offers.
        """
        if lat is not None and lng is not None:
            return self.offers_repository.get_active_offers_nearby(lat, lng, radius_km, limit, offset)
        return self.offers_repository.get_active_offers_paginated(limit, offset)
