from uuid import uuid4

from users.application.dtos.create_user import CreateUserCommand
from users.application.dtos.user_output import UserOutputDTO
from users.application.ports.user_repository import UserRepositoryPort
from users.domain.entities.user import User


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository

    def execute(self, command: CreateUserCommand) -> UserOutputDTO:
        user = User(
            id=str(uuid4()),
            auth0_user_id=command.auth0_user_id,
            email=command.email,
            full_name=command.full_name,
            tipo_documento=command.tipo_documento,
            numero_documento=command.numero_documento,
        )

        created_user = self._user_repository.create(user)

        return UserOutputDTO(
            user_id=created_user.id,
            auth0_user_id=created_user.auth0_user_id,
            email=created_user.email,
            full_name=created_user.full_name,
            tipo_documento=created_user.tipo_documento,
            numero_documento=created_user.numero_documento,
            is_active=created_user.is_active,
        )
