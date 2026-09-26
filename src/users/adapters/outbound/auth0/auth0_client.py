import time

import httpx

from users.application.dtos.auth0_user import Auth0UserResponse
from users.application.ports.auth0_client import Auth0ClientPort
from users.infrastructure.config.settings import settings


class Auth0Client(Auth0ClientPort):
    def __init__(self) -> None:
        self._token_url = f"https://{settings.auth0_domain}/oauth/token"
        self._access_token: str | None = None
        self._token_expires_at: float = 0

    def get_management_token(self) -> str:
        now = time.time()

        if self._access_token and now < self._token_expires_at:
            return self._access_token

        payload = {
            "client_id": settings.auth0_client_id,
            "client_secret": settings.auth0_client_secret,
            "audience": settings.auth0_audience,
            "grant_type": "client_credentials",
        }

        response = httpx.post(
            self._token_url,
            json=payload,
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        self._access_token = data["access_token"]
        self._token_expires_at = now + data["expires_in"] - 60

        return self._access_token

    def create_user(
        self,
        email: str,
        password: str,
        connection: str,
    ) -> Auth0UserResponse:
        token = self.get_management_token()

        payload = {
            "email": email,
            "password": password,
            "connection": connection,
        }

        response = httpx.post(
            f"https://{settings.auth0_domain}/api/v2/users",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=payload,
            timeout=10.0,
        )

        if response.is_error:
            raise RuntimeError(
                f"Auth0 error ({response.status_code}): {response.text}"
            )

        data = response.json()

        return Auth0UserResponse(
            user_id=data["user_id"],
            email=data["email"],
        )