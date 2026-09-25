from fastapi import FastAPI

from users.adapters.inbound.http.exceptions import (
    user_conflict_exception_handler,
    user_not_found_exception_handler,
)
from users.adapters.inbound.http.routes.users import router as users_router
from users.application.exceptions.user_exceptions import (
    UserConflictError,
    UserNotFoundApplicationError,
)

app = FastAPI(
    title="Servicio de Usuarios - Diálisis",
    description="Microservicio de usuarios y Arquitectura Hexagonal",
    version="1.0.0",
)

app.include_router(users_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "users-microservice"}


app.add_exception_handler(
    UserConflictError,
    user_conflict_exception_handler,
)

app.add_exception_handler(
    UserNotFoundApplicationError,
    user_not_found_exception_handler,
)
