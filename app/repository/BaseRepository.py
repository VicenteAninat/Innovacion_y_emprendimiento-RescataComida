"""Base Repository.

This module defines the BaseRepository class, which wraps basic CRUD operations using the Supabase client.
"""

from typing import TypeVar, Generic, Type, List, Optional, Any
from pydantic import BaseModel
from app.config.supabase_client import supabase

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    """Generic base repository defining common CRUD operations on Supabase tables.

    Attributes:
        model_class (Type[T]): The Pydantic model representing the entity class.
        table_name (str): The name of the Supabase table.
    """

    def __init__(self, model_class: Type[T], table_name: str):
        """Initializes the repository with the model class and target table name.

        Args:
            model_class (Type[T]): Pydantic model class.
            table_name (str): Supabase table name.
        """
        self.model_class = model_class
        self.table_name = table_name

    def get_all(self) -> List[T]:
        """Fetches all records from the table.

        Returns:
            List[T]: A list of entity instances.
        """
        response = supabase.table(self.table_name).select("*").execute()
        return [self.model_class(**item) for item in response.data]

    def get_by_id(self, id_val: Any, id_column: str = "id") -> Optional[T]:
        """Fetches a single record matching the given ID.

        Args:
            id_val (Any): The value to search for.
            id_column (str): The column name to match. Defaults to "id".

        Returns:
            Optional[T]: The entity instance if found, otherwise None.
        """
        response = supabase.table(self.table_name).select("*").eq(id_column, id_val).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def create(self, entity: T) -> T:
        """Inserts a new record into the table.

        Args:
            entity (T): The entity instance to create.

        Returns:
            T: The created entity instance returned from the database.
        """
        # Compatibilidad con Pydantic v1 y v2
        if hasattr(entity, "model_dump"):
            data = entity.model_dump(exclude_none=True)
        else:
            data = entity.dict(exclude_none=True)
            
        if "id" in data and data["id"] is None:
            del data["id"]
            
        response = supabase.table(self.table_name).insert(data).execute()
        return self.model_class(**response.data[0])

    def update(self, id_val: Any, update_data: dict, id_column: str = "id") -> Optional[T]:
        """Updates fields of a record matching the given ID.

        Args:
            id_val (Any): The identifier value.
            update_data (dict): Dictionary mapping column names to updated values.
            id_column (str): The identifier column name. Defaults to "id".

        Returns:
            Optional[T]: The updated entity instance if found, otherwise None.
        """
        response = supabase.table(self.table_name).update(update_data).eq(id_column, id_val).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def delete(self, id_val: Any, id_column: str = "id") -> bool:
        """Deletes a record matching the given ID.

        Args:
            id_val (Any): The identifier value.
            id_column (str): The identifier column name. Defaults to "id".

        Returns:
            bool: True if at least one row was deleted, False otherwise.
        """
        response = supabase.table(self.table_name).delete().eq(id_column, id_val).execute()
        return len(response.data) > 0
