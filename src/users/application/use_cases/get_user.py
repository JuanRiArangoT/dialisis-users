from users.application.dtos.user_output import UserOutputDTO
from users.application.ports.user_repository import UserRepositoryPort


class GetUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository

    def execute(self, user_id: str) -> UserOutputDTO | None:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            return None

        return UserOutputDTO(
            user_id=user.id,
            auth0_user_id=user.auth0_user_id,
            email=user.email,
            full_name=user.full_name,
            tipo_documento=user.tipo_documento,
            numero_documento=user.numero_documento,
            is_active=user.is_active,
        )
