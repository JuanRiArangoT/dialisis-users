from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    email: str | None = None
    full_name: str | None = None
    tipo_documento: str | None = None
    numero_documento: str | None = None
    role_id: str | None = None
    is_active: bool | None = None