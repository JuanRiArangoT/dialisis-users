from users.application.dtos.update_user import UpdateUserCommand
from users.application.dtos.user_output import UserOutputDTO
from users.application.exceptions.user_exceptions import (
    UserConflictError,
    UserNotFoundApplicationError,
)
from users.application.ports.role_service import RoleServicePort
from users.application.ports.user_repository import UserRepositoryPort
from users.application.services.user_auth0_service import UserAuth0Service
from users.domain.entities.user import User
from users.domain.exceptions.user_exceptions import UserAlreadyExistsError


class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        auth0_service: UserAuth0Service,
        role_service: RoleServicePort,
    ) -> None:
        self._user_repository = user_repository
        self._auth0_service = auth0_service
        self._role_service = role_service

    def execute(
        self,
        command: UpdateUserCommand,
        auth0_user_id: str | None = None,
    ) -> UserOutputDTO:
        current_user = self._user_repository.get_by_id(command.user_id)

        if current_user is None:
            raise UserNotFoundApplicationError(f"User not found: {command.user_id}")

        if auth0_user_id is not None and current_user.auth0_user_id != auth0_user_id:
            raise UserNotFoundApplicationError(f"User not found: {command.user_id}")

        email = (
            command.email if command.email is not None else current_user.email
        )

        full_name = (
            command.full_name
            if command.full_name is not None
            else current_user.full_name
        )

        tipo_documento = (
            command.tipo_documento
            if command.tipo_documento is not None
            else current_user.tipo_documento
        )

        numero_documento = (
            command.numero_documento
            if command.numero_documento is not None
            else current_user.numero_documento
        )

        role_id = (
            command.role_id
            if command.role_id is not None
            else current_user.role_id
        )

        is_active = (
            command.is_active
            if command.is_active is not None
            else current_user.is_active
        )

        if email != current_user.email:
            existing_user = self._user_repository.get_by_email_excluding_id(
                email,
                command.user_id,
            )

            if existing_user:
                raise UserConflictError("A user with this email already exists.")

            self._auth0_service.update_identity(
                user_id=current_user.auth0_user_id,
                email=email,
            )

        if numero_documento and numero_documento != current_user.numero_documento:
            existing_user = self._user_repository.get_by_document_number_excluding_id(
                numero_documento,
                command.user_id,
            )

            if existing_user:
                raise UserConflictError(
                    "A user with this document number already exists."
                )

        if (
            role_id is not None
            and role_id != current_user.role_id
            and not self._role_service.role_exists(role_id)
        ):
            raise UserConflictError(f"Role not found: {role_id}")

        user = User(
            id=current_user.id,
            auth0_user_id=current_user.auth0_user_id,
            email=email,
            full_name=full_name,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            role_id=role_id,
            is_active=is_active,
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
            role_id=updated_user.role_id,
            is_active=updated_user.is_active,
        )