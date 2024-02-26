from abc import ABC, abstractproperty

from pydantic import BaseModel


class BaseDomainModel(BaseModel, ABC):
    """The base domain model.

    This class is the base class for all domain models in the application.
    """

    @abstractproperty
    def self_id(self) -> int | None:
        """The alias of unique identifier for the domain model.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the domain model.
        """
        pass
