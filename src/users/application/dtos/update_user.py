from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserCommand:
    user_id: str
    email: str
    full_name: str
    tipo_documento: str | None = None
    numero_documento: str | None = None
    is_active: bool = True
