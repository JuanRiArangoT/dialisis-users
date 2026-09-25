from users.application.dtos.user_output import UserOutputDTO
from users.application.exceptions.user_exceptions import (
    UserNotFoundApplicationError,
)
from users.application.ports.user_repository import UserRepositoryPort


class GetUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository

    def execute(self, user_id: str) -> UserOutputDTO:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundApplicationError(f"User not found: {user_id}")

        return UserOutputDTO(
            user_id=user.id,
            auth0_user_id=user.auth0_user_id,
            email=user.email,
            full_name=user.full_name,
            tipo_documento=user.tipo_documento,
            numero_documento=user.numero_documento,
            is_active=user.is_active,
        )
