from unittest.mock import MagicMock, patch

from users.adapters.outbound.roles.role_http_client import RoleHttpClient


def test_role_exists_returns_true() -> None:
    client = RoleHttpClient("http://roles")

    response = MagicMock()
    response.status_code = 200

    with patch("httpx.get", return_value=response) as http_get:
        result = client.role_exists("role-1")

    assert result is True
    http_get.assert_called_once_with(
        "http://roles/roles/role-1",
        timeout=5.0,
    )


def test_has_permission_returns_true() -> None:
    client = RoleHttpClient("http://roles")

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "has_permission": True,
    }

    with patch("httpx.get", return_value=response) as http_get:
        result = client.has_permission(
            "role-1",
            "users.read",
        )

    assert result is True
    http_get.assert_called_once_with(
        "http://roles/roles/role-1/permissions/users.read",
        timeout=5.0,
    )


def test_has_permission_returns_false() -> None:
    client = RoleHttpClient("http://roles")

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "has_permission": False,
    }

    with patch("httpx.get", return_value=response):
        result = client.has_permission(
            "role-1",
            "users.read",
        )

    assert result is False


def test_has_permission_returns_false_when_not_found() -> None:
    client = RoleHttpClient("http://roles")

    response = MagicMock()
    response.status_code = 404

    with patch("httpx.get", return_value=response):
        result = client.has_permission(
            "role-1",
            "users.read",
        )

    assert result is False