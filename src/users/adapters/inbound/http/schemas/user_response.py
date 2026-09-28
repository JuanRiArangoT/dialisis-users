from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: str
    auth0_user_id: str
    email: str
    full_name: str
    tipo_documento: str | None
    numero_documento: str | None
    role_id: str | None = None
    is_active: bool