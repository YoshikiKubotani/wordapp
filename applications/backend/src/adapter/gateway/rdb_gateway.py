from abc import ABC, abstractmethod
from typing import Any


class RDBRepositoryGateway(ABC):
    @classmethod
    @abstractmethod
    def create_connection(cls) -> Any:
        pass

    @abstractmethod
    def select_data(self, conditions: dict[str, Any] = {}) -> list[Any]:
        pass

    @abstractmethod
    def insert_or_update_data(self, data: Any) -> bool:
        pass

    @abstractmethod
    def is_exist(self, conditions: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_data(self, conditions: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_new_id(self) -> int:
        pass

    @abstractmethod
    def create_table(self) -> None:
        pass