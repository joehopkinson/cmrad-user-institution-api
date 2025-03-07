import uuid

from cmrad_user_institution_api.domain import models
from cmrad_user_institution_api.domain import (
    user_institution_association as user_institution_association_entity,
)


class User:
    """Entity object representing an instantiated user in the system.
    The creation of a new user is handled by the factory function below.
    We don't do any validation here as this is the responsibility of the service layer.
    """

    def __init__(
        self, user_id: str, first_name: str, last_name: str, email_address: str
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address

    def validate_institution_association(
        self,
        proposed_association: user_institution_association_entity.UserInstitutionAssociation,
        existing_associations: list[
            user_institution_association_entity.UserInstitutionAssociation
        ],
    ) -> None:
        """Validate that a user can be associated with one primary institution."""
        if proposed_association.is_primary:
            for association in existing_associations:
                if association.is_primary:
                    raise ValueError(
                        f"User {self.user_id} is already associated with a primary institution"
                    )

    def as_dict(self) -> dict[str, str]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
        }


class UserFactory:
    @staticmethod
    def create_user(**kwargs) -> User:
        """Factory function to create a new User object."""
        user_id = str(uuid.uuid4())
        UserFactory.validate_properties(**kwargs)
        return User(user_id, **kwargs)

    @staticmethod
    def validate_properties(**kwargs):
        for key, value in kwargs.items():
            if key == "email_address":
                valid_email_address = models.EmailAddress(value=value)
                kwargs[key] = valid_email_address.value
        return kwargs
