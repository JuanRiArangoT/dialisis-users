from fastapi import FastAPI

app = FastAPI(
    title="Servicio de Usuarios - Diálisis",
    description="Microservicio de usuarios y Arquitectura Hexagonal",
    version="1.0.0",
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "users-microservice"}