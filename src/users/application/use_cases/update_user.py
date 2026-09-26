from users.application.dtos.update_user import UpdateUserCommand
from users.application.dtos.user_output import UserOutputDTO
from users.application.exceptions.user_exceptions import (
    UserConflictError,
    UserNotFoundApplicationError,
)
from users.application.ports.user_repository import UserRepositoryPort
from users.domain.entities.user import User
from users.domain.exceptions.user_exceptions import UserAlreadyExistsError


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository

    def execute(
        self,
        command: UpdateUserCommand,
        auth0_user_id: str | None = None,
    ) -> UserOutputDTO:
        current_user = self._user_repository.get_by_id(command.user_id)

        if current_user is None:
            raise UserNotFoundApplicationError(f"User not found: {command.user_id}")

        if auth0_user_id is not None and current_user.auth0_user_id != auth0_user_id:
            raise UserNotFoundApplicationError(
                f"User not found: {command.user_id}"
            )

        existing_user = self._user_repository.get_by_email_excluding_id(
            command.email,
            command.user_id,
        )

        if existing_user:
            raise UserConflictError("A user with this email already exists.")

        if command.numero_documento:
            existing_user = self._user_repository.get_by_document_number_excluding_id(
                command.numero_documento,
                command.user_id,
            )

            if existing_user:
                raise UserConflictError(
                    "A user with this document number already exists."
                )

        user = User(
            id=current_user.id,
            auth0_user_id=current_user.auth0_user_id,
            email=command.email,
            full_name=command.full_name,
            tipo_documento=command.tipo_documento,
            numero_documento=command.numero_documento,
            is_active=command.is_active,
        )

        try:
            updated_user = self._user_repository.update(user)
        except UserAlreadyExistsError as exc:
            raise UserConflictError(str(exc)) from exc

        return UserOutputDTO(
            user_id=updated_user.id,
            auth0_user_id=updated_user.auth0_user_id,
            email=updated_user.email,
            full_name=updated_user.full_name,
            tipo_documento=updated_user.tipo_documento,
            numero_documento=updated_user.numero_documento,
            is_active=updated_user.is_active,
        )
