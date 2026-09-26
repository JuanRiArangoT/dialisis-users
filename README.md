# dialisis-users

Microservicio de gestión de usuarios para la plataforma Dialisis, desarrollado con Python y FastAPI bajo una arquitectura hexagonal.

## Tecnologías

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL 16
* Alembic
* Auth0
* Pytest
* Ruff
* Docker
* Docker Compose
* uv

## Arquitectura

El proyecto sigue los principios de Arquitectura Hexagonal, separando el dominio, la lógica de aplicación, los adaptadores de entrada/salida y la infraestructura.

```text
src/users/
├── adapters/
│   ├── inbound/
│   │   └── http/
│   └── outbound/
│       ├── auth0/
│       └── database/
├── application/
│   ├── dtos/
│   ├── exceptions/
│   ├── ports/
│   ├── services/
│   └── use_cases/
├── domain/
├── infrastructure/
└── main.py
```

## Requisitos

Para ejecutar el proyecto localmente se requiere:

* Python 3.13+
* uv
* Docker y Docker Compose

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/dialisis_users
POSTGRES_PASSWORD=postgres

AUTH0_DOMAIN=<auth0-domain>
AUTH0_CLIENT_ID=<auth0-client-id>
AUTH0_CLIENT_SECRET=<auth0-client-secret>
AUTH0_AUDIENCE=<auth0-audience>
AUTH0_DB_CONNECTION=Username-Password-Authentication
```

> No subir archivos `.env` al repositorio. Las credenciales y secretos deben mantenerse fuera del control de versiones.

## Ejecución con Docker

Construir las imágenes:

```bash
docker compose build
```

Iniciar los servicios:

```bash
docker compose up -d
```

Los servicios quedan disponibles en:

```text
Users API: http://localhost:8001
PostgreSQL: localhost:5432
```

Verificar el estado de los contenedores:

```bash
docker compose ps
```

Detener los servicios:

```bash
docker compose down
```

## Base de datos y migraciones

Aplicar las migraciones:

```bash
docker compose exec users uv run alembic upgrade head
```

Consultar la versión actual de la base de datos:

```bash
docker compose exec users uv run alembic current
```

Crear una nueva migración:

```bash
docker compose exec users uv run alembic revision --autogenerate -m "description"
```

## API

### Health Check

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "users-microservice"
}
```

### Obtener usuario autenticado

```http
GET /users/me
Authorization: Bearer <access_token>
```

Obtiene la información del usuario asociado al `sub` del token de Auth0.

Respuesta:

```json
{
  "user_id": "uuid",
  "auth0_user_id": "auth0|...",
  "email": "usuario@example.com",
  "full_name": "Nombre Usuario",
  "tipo_documento": "CC",
  "numero_documento": "123456789",
  "is_active": true
}
```

## Ejecución local sin Docker

Instalar las dependencias:

```bash
uv sync
```

Ejecutar el servidor:

```bash
uv run uvicorn users.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

## Pruebas

Ejecutar todos los tests:

```bash
uv run pytest
```

## Linter

Ejecutar Ruff:

```bash
uv run ruff check .
```

## Documentación de la API

Con el servidor ejecutándose, FastAPI proporciona automáticamente:

```text
Swagger UI: http://localhost:8001/docs
ReDoc:       http://localhost:8001/redoc
```

Si se ejecuta sin Docker, utilizar el puerto `8000`.

## Estructura de Docker

El proyecto utiliza dos servicios mediante Docker Compose:

```text
┌──────────────────────────┐
│      dialisis-users      │
│        FastAPI           │
│       port: 8000         │
└────────────┬─────────────┘
             │
             │ PostgreSQL
             ▼
┌──────────────────────────┐
│   dialisis-users-db      │
│      PostgreSQL 16       │
│       port: 5432         │
└──────────────────────────┘
```

Desde el equipo local, la API se expone mediante el puerto `8001`:

```text
localhost:8001 → users:8000
```

## Estado del proyecto

Actualmente el microservicio cuenta con:

* Gestión de usuarios.
* Persistencia mediante PostgreSQL.
* Migraciones mediante Alembic.
* Autenticación e integración con Auth0.
* Endpoint para consultar el usuario autenticado.
* Tests automatizados.
* Linter con Ruff.
* Contenerización mediante Docker.
* Orquestación mediante Docker Compose.
