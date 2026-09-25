class UserConflictError(Exception):
    """Raised when a user conflicts with an existing record."""


class UserNotFoundApplicationError(Exception):
    """Raised when a user cannot be found."""
