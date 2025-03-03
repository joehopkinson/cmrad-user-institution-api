import uuid

from cmrad_user_institution_api.domain import models


class User:
    """Entity object representing a user in the system.
    This object represents an instantiated user, rather than the creation of a new one
    which is handled by the factory function below. As such, we don't do any validation here
    as this is the responsibility of the service layer.
    """

    def __init__(
        self, user_id: str, first_name: str, last_name: str, email_address: str
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address


def create_user(first_name: str, last_name: str, email_address: str) -> User:
    """Factory function to create a new User object."""
    user_id = str(uuid.uuid4())

    # Perform domain specific validation here
    email_address = models.EmailAddress(value=email_address)

    return User(user_id, first_name, last_name, email_address.value)
