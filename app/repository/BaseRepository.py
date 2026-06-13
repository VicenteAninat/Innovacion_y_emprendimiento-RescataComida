from typing import TypeVar, Generic, Type, List, Optional, Any
from pydantic import BaseModel
from app.config.supabase_client import supabase

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], table_name: str):
        self.model_class = model_class
        self.table_name = table_name

    def get_all(self) -> List[T]:
        response = supabase.table(self.table_name).select("*").execute()
        return [self.model_class(**item) for item in response.data]

    def get_by_id(self, id_val: Any, id_column: str = "id") -> Optional[T]:
        response = supabase.table(self.table_name).select("*").eq(id_column, id_val).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def create(self, entity: T) -> T:
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
        response = supabase.table(self.table_name).update(update_data).eq(id_column, id_val).execute()
        if not response.data:
            return None
        return self.model_class(**response.data[0])

    def delete(self, id_val: Any, id_column: str = "id") -> bool:
        response = supabase.table(self.table_name).delete().eq(id_column, id_val).execute()
        return len(response.data) > 0
