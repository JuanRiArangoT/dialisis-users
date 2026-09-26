from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from users.adapters.inbound.http.dependencies.auth0_jwt import get_current_user
from users.adapters.inbound.http.dependencies.database import get_db
from users.adapters.inbound.http.schemas.create_user import CreateUserRequest
from users.adapters.inbound.http.schemas.update_user import UpdateUserRequest
from users.adapters.inbound.http.schemas.user_response import UserResponse
from users.adapters.outbound.database.user_repository import PostgresUserRepository
from users.application.dtos.create_user import CreateUserCommand
from users.application.dtos.update_user import UpdateUserCommand
from users.application.use_cases.create_user import CreateUserUseCase
from users.application.use_cases.delete_user import DeleteUserUseCase
from users.application.use_cases.get_user import GetUserUseCase
from users.application.use_cases.update_user import UpdateUserUseCase

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
    use_case = CreateUserUseCase(repository)

    command = CreateUserCommand(
        auth0_user_id=request.auth0_user_id,
        email=request.email,
        full_name=request.full_name,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
    )

    result = use_case.execute(command)

    return UserResponse(
        user_id=result.user_id,
        auth0_user_id=result.auth0_user_id,
        email=result.email,
        full_name=result.full_name,
        tipo_documento=result.tipo_documento,
        numero_documento=result.numero_documento,
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
    use_case = UpdateUserUseCase(repository)

    command = UpdateUserCommand(
        user_id=user_id,
        email=request.email,
        full_name=request.full_name,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
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
