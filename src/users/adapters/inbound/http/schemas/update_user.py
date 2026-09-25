from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    email: str
    full_name: str
    tipo_documento: str | None = None
    numero_documento: str | None = None
    is_active: bool = True
