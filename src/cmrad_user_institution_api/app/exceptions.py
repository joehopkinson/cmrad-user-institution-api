class UserNotFoundError(Exception):
    """Raised when a user is not found."""


class InstitutionNotFoundError(Exception):
    """Raised when an institution is not found."""


class ExistingUserInstitutionAssociationError(Exception):
    """Raised when a user-institution association already exists."""


class UserUpdateError(Exception):
    """Raised when a user update fails."""


class InstitutionUpdateError(Exception):
    """Raised when an institution update fails."""


class InvalidUserInstitutionAssociationError(Exception):
    """Raised when an invalid user-institution association is detected."""
