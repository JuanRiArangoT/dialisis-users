from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from users.adapters.inbound.http.dependencies.auth0_jwt import get_current_user
from users.adapters.inbound.http.dependencies.authorization import (
    require_permission,
)
from users.adapters.inbound.http.dependencies.database import get_db
from users.adapters.inbound.http.schemas.create_user import CreateUserRequest
from users.adapters.inbound.http.schemas.update_user import UpdateUserRequest
from users.adapters.inbound.http.schemas.user_response import UserResponse
from users.adapters.outbound.auth0.auth0_client import Auth0Client
from users.adapters.outbound.database.user_repository import PostgresUserRepository
from users.adapters.outbound.roles.role_http_client import RoleHttpClient
from users.application.dtos.create_user import CreateUserCommand
from users.application.dtos.update_user import UpdateUserCommand
from users.application.services.user_auth0_service import UserAuth0Service
from users.application.use_cases.create_user import CreateUserUseCase
from users.application.use_cases.delete_user import DeleteUserUseCase
from users.application.use_cases.get_user import GetUserUseCase
from users.application.use_cases.update_user import UpdateUserUseCase
from users.infrastructure.config.settings import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    repository = PostgresUserRepository(db)
    role_service = RoleHttpClient(settings.roles_service_url)

    use_case = CreateUserUseCase(
        repository,
        role_service,
    )

    command = CreateUserCommand(
        auth0_user_id=request.auth0_user_id,
        email=request.email,
        full_name=request.full_name,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
        role_id=request.role_id,
    )

    result = use_case.execute(command)

    return UserResponse(
        user_id=result.user_id,
        auth0_user_id=result.auth0_user_id,
        email=result.email,
        full_name=result.full_name,
        tipo_documento=result.tipo_documento,
        numero_documento=result.numero_documento,
        role_id=result.role_id,
        is_active=result.is_active,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.read"))],
)
def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    repository = PostgresUserRepository(db)
    use_case = GetUserUseCase(repository)

    result = use_case.execute(
        auth0_user_id=current_user["sub"],
    )

    return UserResponse(
        user_id=result.user_id,
        auth0_user_id=result.auth0_user_id,
        email=result.email,
        full_name=result.full_name,
        tipo_documento=result.tipo_documento,
        numero_documento=result.numero_documento,
        role_id=result.role_id,
        is_active=result.is_active,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    repository = PostgresUserRepository(db)
    use_case = GetUserUseCase(repository)

    result = use_case.execute(
        user_id=user_id,
        auth0_user_id=current_user["sub"],
    )

    return UserResponse(
        user_id=result.user_id,
        auth0_user_id=result.auth0_user_id,
        email=result.email,
        full_name=result.full_name,
        tipo_documento=result.tipo_documento,
        numero_documento=result.numero_documento,
        role_id=result.role_id,
        is_active=result.is_active,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: str,
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    repository = PostgresUserRepository(db)
    auth0_client = Auth0Client()
    auth0_service = UserAuth0Service(auth0_client)
    role_service = RoleHttpClient(settings.roles_service_url)

    use_case = UpdateUserUseCase(
        user_repository=repository,
        auth0_service=auth0_service,
        role_service=role_service,
    )

    command = UpdateUserCommand(
        user_id=user_id,
        email=request.email,
        full_name=request.full_name,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
        role_id=request.role_id,
        is_active=request.is_active,
    )

    result = use_case.execute(
        command=command,
        auth0_user_id=current_user["sub"],
    )

    return UserResponse(
        user_id=result.user_id,
        auth0_user_id=result.auth0_user_id,
        email=result.email,
        full_name=result.full_name,
        tipo_documento=result.tipo_documento,
        numero_documento=result.numero_documento,
        role_id=result.role_id,
        is_active=result.is_active,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> None:
    repository = PostgresUserRepository(db)
    use_case = DeleteUserUseCase(repository)

    use_case.execute(
        user_id=user_id,
        auth0_user_id=current_user["sub"],
    )
