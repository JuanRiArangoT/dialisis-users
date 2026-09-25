from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand:
    auth0_user_id: str
    email: str
    full_name: str
    tipo_documento: str | None = None
    numero_documento: str | None = None
