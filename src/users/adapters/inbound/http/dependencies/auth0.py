from users.adapters.outbound.auth0.auth0_client import Auth0Client
from users.application.services.user_auth0_service import UserAuth0Service


def get_auth0_service() -> UserAuth0Service:
    return UserAuth0Service(
        auth0_client=Auth0Client(),
    )