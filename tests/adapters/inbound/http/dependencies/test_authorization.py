from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from users.adapters.inbound.http.dependencies.authorization import (
    require_permission,
)


def test_require_permission_allows_user_with_permission() -> None:
    dependency = require_permission("users.read")

    current_user = {"sub": "auth0|123"}
    user = Mock(role_id="role-123")

    with (
        patch(
            "users.adapters.inbound.http.dependencies.authorization.PostgresUserRepository"
        ) as repository_class,
        patch(
            "users.adapters.inbound.http.dependencies.authorization.RoleHttpClient"
        ) as role_client_class,
    ):
        repository_class.return_value.get_by_auth0_id.return_value = user
        role_client_class.return_value.has_permission.return_value = True

        dependency(
            current_user=current_user,
            db=Mock(),
        )

        role_client_class.return_value.has_permission.assert_called_once_with(
            role_id="role-123",
            permission_name="users.read",
        )


def test_require_permission_denies_user_without_permission() -> None:
    dependency = require_permission("users.read")

    current_user = {"sub": "auth0|123"}
    user = Mock(role_id="role-123")

    with (
        patch(
            "users.adapters.inbound.http.dependencies.authorization.PostgresUserRepository"
        ) as repository_class,
        patch(
            "users.adapters.inbound.http.dependencies.authorization.RoleHttpClient"
        ) as role_client_class,
    ):
        repository_class.return_value.get_by_auth0_id.return_value = user
        role_client_class.return_value.has_permission.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            dependency(
                current_user=current_user,
                db=Mock(),
            )

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Insufficient permissions"


def test_require_permission_denies_user_without_role() -> None:
    dependency = require_permission("users.read")

    current_user = {"sub": "auth0|123"}
    user = Mock(role_id=None)

    with patch(
        "users.adapters.inbound.http.dependencies.authorization.PostgresUserRepository"
    ) as repository_class:
        repository_class.return_value.get_by_auth0_id.return_value = user

        with pytest.raises(HTTPException) as exc_info:
            dependency(
                current_user=current_user,
                db=Mock(),
            )

        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "User has no assigned role"


def test_require_permission_denies_unknown_user() -> None:
    dependency = require_permission("users.read")

    current_user = {"sub": "auth0|123"}

    with patch(
        "users.adapters.inbound.http.dependencies.authorization.PostgresUserRepository"
    ) as repository_class:
        repository_class.return_value.get_by_auth0_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            dependency(
                current_user=current_user,
                db=Mock(),
            )

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "User not found"