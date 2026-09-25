from fastapi import FastAPI

from users.adapters.inbound.http.routes.users import router as users_router

app = FastAPI(
    title="Servicio de Usuarios - Diálisis",
    description="Microservicio de usuarios y Arquitectura Hexagonal",
    version="1.0.0",
)

app.include_router(users_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "users-microservice"}
