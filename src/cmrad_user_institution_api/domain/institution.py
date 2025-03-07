import uuid
from typing import Any


class Institution:
    """Entity object representing an instantiated institution in the system.
    The creation of a new institution is handled by the factory function below.
    We don't do any validation here as this is the responsibility of the service layer.
    """

    def __init__(self, institution_id: str, institution_name: str, user_count: int = 0):
        self.institution_id = institution_id
        self.institution_name = institution_name
        self.user_count = user_count

    def as_dict(self) -> dict[str, Any]:
        return {
            "institution_id": self.institution_id,
            "institution_name": self.institution_name,
            "user_count": self.user_count,
        }


class InstitutionFactory:
    @staticmethod
    def create_institution(**kwargs) -> Institution:
        """Factory function to create a new User object."""
        institution_id = str(uuid.uuid4())

        return Institution(institution_id, **kwargs)

    @staticmethod
    def validate_properties(**kwargs) -> dict[str, Any]:
        """Validate the properties of an institution object."""
        for key, value in kwargs.items():
            if key == "user_count":
                raise ValueError("User count is a read-only property")
        return kwargs
