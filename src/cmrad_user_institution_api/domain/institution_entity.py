import uuid


class Institution:
    """Entity object representing an instantiated institution in the system.
    The creation of a new institution is handled by the factory function below.
    We don't do any validation here as this is the responsibility of the service layer.
    """

    def __init__(self, institution_id: str, institution_name: str):
        self.institution_id = institution_id
        self.institution_name = institution_name

    def as_dict(self) -> dict[str, str]:
        return {
            "institution_id": self.institution_id,
            "institution_name": self.institution_name,
        }


class InstitutionFactory:
    @staticmethod
    def create_institution(institution_name: str) -> Institution:
        """Factory function to create a new User object."""
        institution_id = str(uuid.uuid4())

        return Institution(institution_id, institution_name)
