from users.application.exceptions.user_exceptions import (
    UserNotFoundApplicationError,
)
from users.application.ports.user_repository import UserRepositoryPort


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository


    def execute(
        self,
        user_id: str,
        auth0_user_id: str | None = None,
    ) -> None:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundApplicationError(f"User not found: {user_id}")

        if auth0_user_id is not None and user.auth0_user_id != auth0_user_id:
            raise UserNotFoundApplicationError(f"User not found: {user_id}")

        self._user_repository.delete(user_id)

