from typing import Protocol

from users.application.dtos.auth0_user import Auth0UserResponse


class Auth0ClientPort(Protocol):
    def get_management_token(self) -> str:
        ...

    def create_user(
        self,
        email: str,
        password: str,
        connection: str,
    ) -> Auth0UserResponse:
        ...