from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from users.adapters.inbound.http.dependencies.auth0_jwt import get_current_user
from users.adapters.inbound.http.dependencies.database import get_db
from users.adapters.outbound.database.user_repository import PostgresUserRepository
from users.adapters.outbound.roles.role_http_client import RoleHttpClient
from users.application.ports.authorization_service import AuthorizationServicePort
from users.infrastructure.config.settings import settings


def require_permission(
    permission_name: str,
) -> Callable:
    def dependency(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> None:
        repository = PostgresUserRepository(db)

        user = repository.get_by_auth0_id(current_user["sub"])

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if user.role_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role",
            )

        authorization_service: AuthorizationServicePort = RoleHttpClient(
            settings.roles_service_url,
        )

        if not authorization_service.has_permission(
            role_id=user.role_id,
            permission_name=permission_name,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

    return dependency