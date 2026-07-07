"""Donations Service.

This module defines the DonationsService class which handles business logic for donations.
"""

from typing import List, Optional
from app.entity.DonationsEntity import DonationsEntity
from app.repository.DonationsRepository import DonationsRepository

class DonationsService:
    """Service class encapsulating logic for food surplus donations."""

    def __init__(self):
        """Initializes the service by setting up the DonationsRepository."""
        self.donations_repository = DonationsRepository()

    def get_all_donations(self) -> List[DonationsEntity]:
        """Retrieves all registered donations in the system.

        Returns:
            List[DonationsEntity]: List of all donations.
        """
        return self.donations_repository.get_all()

    def get_donation_by_id(self, id_val: int) -> Optional[DonationsEntity]:
        """Fetches a donation using its unique ID.

        Args:
            id_val (int): ID of the donation record.

        Returns:
            Optional[DonationsEntity]: The donation record if found, otherwise None.
        """
        return self.donations_repository.get_by_id(id_val)

    def get_donations_by_business(self, business_id: int) -> List[DonationsEntity]:
        """Retrieves donation history for a specific business.

        Args:
            business_id (int): Unique identifier of the business.

        Returns:
            List[DonationsEntity]: List of donations matching the business.
        """
        return self.donations_repository.get_by_business_id(business_id)

    def create_donation(self, business_id: int, food_bank_id: int, description: Optional[str] = None, weight_kg: Optional[float] = None, tax_deductible_receipt_url: Optional[str] = None) -> DonationsEntity:
        """Registers a new donation from a business to a food bank.

        Args:
            business_id (int): ID of the business.
            food_bank_id (int): ID of the target food bank.
            description (Optional[str]): Description of donated items.
            weight_kg (Optional[float]): Estimated total weight in kg.
            tax_deductible_receipt_url (Optional[str]): Receipt document URL.

        Returns:
            DonationsEntity: The created donation details.
        """
        entity = DonationsEntity(
            business_id=business_id,
            food_bank_id=food_bank_id,
            description=description,
            weight_kg=weight_kg,
            tax_deductible_receipt_url=tax_deductible_receipt_url
        )
        return self.donations_repository.create(entity)

    def update_donation(self, id_val: int, data: dict) -> Optional[DonationsEntity]:
        """Updates fields of a donation record.

        Args:
            id_val (int): ID of the donation record.
            data (dict): Dictionary mapping column names to new values.

        Returns:
            Optional[DonationsEntity]: The updated donation record if found, otherwise None.
        """
        return self.donations_repository.update(id_val, data)

    def delete_donation(self, id_val: int) -> bool:
        """Deletes a donation record.

        Args:
            id_val (int): ID of the donation record to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        return self.donations_repository.delete(id_val)
