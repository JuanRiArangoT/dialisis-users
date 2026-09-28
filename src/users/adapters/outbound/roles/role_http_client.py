import httpx

from users.application.ports.role_service import RoleServicePort


class RoleHttpClient(RoleServicePort):
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
