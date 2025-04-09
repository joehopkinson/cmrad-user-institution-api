from typing import Any


class UserInstitutionAssociation:
    """Entity class representing an association between a user and an institution."""

    def __init__(self, user_id: str, institution_id: str, is_primary: bool = False):
        self.user_id = user_id
        self.institution_id = institution_id
        self.is_primary = is_primary

    def set_primary_status(self, is_primary: bool) -> None:
        self.is_primary = is_primary

    def as_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "institution_id": self.institution_id,
            "is_primary": self.is_primary,
        }


class UserInstitutionAssociationFactory:
    @staticmethod
    def create_association(
        user_id: str, institution_id: str, is_primary: bool = False
    ) -> UserInstitutionAssociation:
        """Factory function to create a new UserInstitutionAssociation object."""
        return UserInstitutionAssociation(user_id, institution_id, is_primary)
