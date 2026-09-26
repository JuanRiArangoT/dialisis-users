from users.application.dtos.auth0_user import Auth0UserResponse
from users.application.ports.auth0_client import Auth0ClientPort


class UserAuth0Service:
    """Coordinates user synchronization with Auth0."""

    def __init__(self, auth0_client: Auth0ClientPort) -> None:
        self._auth0_client = auth0_client

    def create_identity(
        self,
        email: str,
        password: str,
        connection: str,
    ) -> Auth0UserResponse:
        return self._auth0_client.create_user(
            email=email,
            password=password,
            connection=connection,
        )