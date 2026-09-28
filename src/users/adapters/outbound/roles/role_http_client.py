import httpx

from users.application.ports.authorization_service import (
    AuthorizationServicePort,
)
from users.application.ports.role_service import RoleServicePort


class RoleHttpClient(
    RoleServicePort,
    AuthorizationServicePort,
):
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def role_exists(self, role_id: str) -> bool:
        response = httpx.get(
            f"{self._base_url}/roles/{role_id}",
            timeout=5.0,
        )

        if response.status_code == 404:
            return False

        response.raise_for_status()

        return True

    def has_permission(
        self,
        role_id: str,
        permission_name: str,
    ) -> bool:
        response = httpx.get(
            f"{self._base_url}/roles/{role_id}/permissions/{permission_name}",
            timeout=5.0,
        )

        if response.status_code == 404:
            return False

        response.raise_for_status()

        data = response.json()

        return bool(data["has_permission"])