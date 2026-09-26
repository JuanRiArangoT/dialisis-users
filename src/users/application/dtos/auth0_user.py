from typing import TypedDict


class Auth0UserResponse(TypedDict):
    user_id: str
    email: str