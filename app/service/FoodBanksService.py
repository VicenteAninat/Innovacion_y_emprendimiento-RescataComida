"""Food Banks Service.

This module defines the FoodBanksService class which manages operations for food bank organizations.
"""

from typing import List, Optional
from app.entity.FoodBanksEntity import FoodBanksEntity
from app.repository.FoodBanksRepository import FoodBanksRepository

class FoodBanksService:
    """Service class encapsulating logic for food bank registration and management."""

    def __init__(self):
        """Initializes the service by setting up the FoodBanksRepository."""
        self.food_banks_repository = FoodBanksRepository()

    def get_all_food_banks(self) -> List[FoodBanksEntity]:
        """Retrieves a list of all food banks.

        Returns:
            List[FoodBanksEntity]: A list of all food banks.
        """
        return self.food_banks_repository.get_all()

    def get_food_bank_by_id(self, id_val: int) -> Optional[FoodBanksEntity]:
        """Fetches a food bank by its unique ID.

        Args:
            id_val (int): ID of the food bank.

        Returns:
            Optional[FoodBanksEntity]: The food bank entity if found, otherwise None.
        """
        return self.food_banks_repository.get_by_id(id_val)

    def create_food_bank(self, rut: str, name: Optional[str] = None, contact_email: Optional[str] = None, contact_phone: Optional[str] = None, address: Optional[str] = None) -> FoodBanksEntity:
        """Registers a new food bank organization.

        Args:
            rut (str): Tax identification number/RUT.
            name (Optional[str]): Commercial name.
            contact_email (Optional[str]): Contact email address.
            contact_phone (Optional[str]): Contact phone number.
            address (Optional[str]): Physical street address.

        Returns:
            FoodBanksEntity: The created food bank entity.
        """
        entity = FoodBanksEntity(
            rut=rut,
            name=name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            address=address
        )
        return self.food_banks_repository.create(entity)

    def update_food_bank(self, id_val: int, data: dict) -> Optional[FoodBanksEntity]:
        """Updates attributes of a food bank.

        Args:
            id_val (int): ID of the food bank.
            data (dict): Dict mapping columns to update.

        Returns:
            Optional[FoodBanksEntity]: The updated food bank entity if found, otherwise None.
        """
        return self.food_banks_repository.update(id_val, data)

    def delete_food_bank(self, id_val: int) -> bool:
        """Deletes a food bank from the system.

        Args:
            id_val (int): ID of the food bank to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        return self.food_banks_repository.delete(id_val)
