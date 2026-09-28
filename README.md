
# Diálisis Users

Microservicio de gestión de usuarios de la plataforma Diálisis, desarrollado con Python y FastAPI bajo los principios de Arquitectura Hexagonal.

Permite administrar usuarios, consultar el perfil del usuario autenticado, sincronizar información con Auth0 y asociar usuarios con roles administrados por el microservicio `dialisis-roles`.

## Tecnologías

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Alembic
- Auth0
- HTTPX
- Pytest
- Ruff
- Docker
- Docker Compose
- uv

## Arquitectura

El proyecto implementa Arquitectura Hexagonal (Ports and Adapters), separando las responsabilidades del dominio, la aplicación, los adaptadores y la infraestructura.

```text
src/
└── users/
    ├── adapters/
    │   ├── inbound/
    │   │   └── http/
    │   │       ├── dependencies/
    │   │       ├── routes/
    │   │       └── schemas/
    │   └── outbound/
    │       ├── auth0/
    │       ├── database/
    │       └── roles/
    ├── application/
    │   ├── dtos/
    │   ├── exceptions/
    │   ├── ports/
    │   ├── services/
    │   └── use_cases/
    ├── domain/
    │   ├── entities/
    │   ├── exceptions/
    │   └── services/
    ├── infrastructure/
    │   └── config/
    └── main.py

migrations/
├── versions/
└── env.py

tests/
```

### Responsabilidades

| Capa | Responsabilidad |
|---|---|
| Domain | Entidades y reglas de negocio del dominio de usuarios. |
| Application | Casos de uso, DTOs, puertos y excepciones de aplicación. |
| Adapters Inbound | Exposición de la API HTTP mediante FastAPI. |
| Adapters Outbound | Integración con PostgreSQL, Auth0 y el servicio de roles. |
| Infrastructure | Configuración y componentes técnicos. |

Los casos de uso dependen de puertos definidos en la aplicación. Los adaptadores implementan esos puertos para comunicarse con los sistemas externos.

## Microservicios relacionados

El microservicio de usuarios se integra con los siguientes componentes:

| Servicio | Responsabilidad |
|---|---|
| dialisis-auth | Autenticación y gestión de credenciales mediante Auth0. |
| dialisis-roles | Administración y consulta de roles. |
| PostgreSQL | Persistencia de los datos de los microservicios. |

### Integración con roles

El microservicio consulta `dialisis-roles` para validar que un rol exista antes de asociarlo a un usuario.

La comunicación se realiza mediante HTTP utilizando la variable `ROLES_SERVICE_URL`.

La relación lógica entre usuarios y roles es:

```text
users.users.role_id
        │
        ▼
roles.roles.id
```

Cada usuario puede tener un `role_id` opcional, correspondiente al identificador de un rol registrado en el microservicio de roles.

La validación de existencia se realiza a través de la API de roles, manteniendo los microservicios desacoplados a nivel de aplicación y modelo ORM.

## Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.13 o superior.
- uv.
- Docker y Docker Compose.
- Acceso a una instancia de PostgreSQL.
- Una aplicación y configuración de Auth0 válidas.

## Configuración

Crear un archivo `.env` en la raíz del proyecto.

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@dialisis-users-db:5432/dialisis

POSTGRES_PASSWORD=postgres

AUTH0_DOMAIN=<auth0-domain>
AUTH0_CLIENT_ID=<auth0-client-id>
AUTH0_CLIENT_SECRET=<auth0-client-secret>
AUTH0_AUDIENCE=<auth0-audience>
AUTH0_API_AUDIENCE=<auth0-api-audience>

ROLES_SERVICE_URL=http://dialisis-roles:8000
```

### Variables de entorno

| Variable | Descripción |
|---|---|
| DATABASE_URL | Cadena de conexión a PostgreSQL. |
| POSTGRES_PASSWORD | Contraseña del usuario de PostgreSQL utilizado por Docker. |
| AUTH0_DOMAIN | Dominio del tenant de Auth0. |
| AUTH0_CLIENT_ID | Identificador de la aplicación de Auth0. |
| AUTH0_CLIENT_SECRET | Secreto de la aplicación de Auth0. |
| AUTH0_AUDIENCE | Audiencia configurada para la autenticación. |
| AUTH0_API_AUDIENCE | Audiencia de la API utilizada por el servicio. |
| ROLES_SERVICE_URL | URL base del microservicio de roles. |

Los valores de Auth0 deben corresponder a la configuración del entorno.

**Importante:** No subir archivos `.env`, secretos, tokens ni credenciales al repositorio. Mantenerlos fuera del control de versiones.

### URLs según el entorno

| Entorno | URL del servicio de roles |
|---|---|
| Docker | `http://dialisis-roles:8000` |
| Ejecución local | `http://localhost:8002` |

Dentro de Docker se utiliza el nombre del contenedor o servicio en la red compartida. Desde el equipo local se utiliza el puerto publicado por Docker Compose.

## Ejecución con Docker

El microservicio utiliza una red Docker externa llamada `dialisis-network` y comparte la base de datos `dialisis` con los demás servicios.

### 1. Construir la imagen

```powershell
docker compose build
```

### 2. Iniciar los servicios

```powershell
docker compose up -d
```

### 3. Verificar los contenedores

```powershell
docker compose ps
```

### 4. Consultar los logs

```powershell
docker compose logs -f users
```

### 5. Detener los servicios

```powershell
docker compose down
```

Este comando detiene los servicios definidos en el Compose. No elimina el volumen de PostgreSQL.

### URLs de acceso

| Componente | Dirección |
|---|---|
| Users API | http://localhost:8001 |
| Swagger UI | http://localhost:8001/docs |
| ReDoc | http://localhost:8001/redoc |
| PostgreSQL | localhost:5432 |

El servicio FastAPI escucha en el puerto `8000` dentro del contenedor y se publica en el puerto `8001` del equipo local.

## Base de datos y migraciones

El microservicio utiliza PostgreSQL y administra sus migraciones mediante Alembic.

La base de datos compartida tiene la siguiente organización lógica:

```text
dialisis
├── users
│   ├── users
│   └── alembic_version
├── roles
│   ├── roles
│   └── alembic_version
├── patients
├── doctors
└── appointments
```

El microservicio de usuarios administra exclusivamente sus tablas dentro del esquema `users`.

### Aplicar migraciones

Con Docker:

```powershell
docker compose exec users uv run alembic upgrade head
```

### Consultar la revisión actual

```powershell
docker compose exec users uv run alembic current
```

### Generar una nueva migración

```powershell
docker compose exec users uv run alembic revision --autogenerate -m "description"
```

Las migraciones generadas deben revisarse antes de aplicarlas.

No se deben eliminar ni recrear los volúmenes de PostgreSQL para aplicar cambios de esquema.

## API

La API está expuesta mediante FastAPI y utiliza esquemas Pydantic para validar las solicitudes y respuestas.

### Health Check

```http
GET /health
```

Verifica el estado del servicio.

Respuesta:

```json
{
  "status": "ok",
  "service": "users-microservice"
}
```

### Crear usuario

```http
POST /users
Content-Type: application/json
```

Ejemplo de solicitud:

```json
{
  "auth0_user_id": "auth0|123456",
  "email": "usuario@example.com",
  "full_name": "Nombre Usuario",
  "tipo_documento": "CC",
  "numero_documento": "123456789",
  "role_id": "uuid-del-rol"
}
```

El campo `role_id` es opcional. Cuando se proporciona, se valida su existencia en `dialisis-roles`.

Respuesta exitosa: `201 Created`.

### Obtener usuario autenticado

```http
GET /users/me
Authorization: Bearer <access_token>
```

Obtiene el perfil del usuario autenticado utilizando el identificador `sub` del token de Auth0.

Respuesta de ejemplo:

```json
{
  "user_id": "uuid",
  "auth0_user_id": "auth0|123456",
  "email": "usuario@example.com",
  "full_name": "Nombre Usuario",
  "tipo_documento": "CC",
  "numero_documento": "123456789",
  "role_id": "uuid-del-rol",
  "is_active": true
}
```

### Obtener usuario por identificador

```http
GET /users/{user_id}
Authorization: Bearer <access_token>
```

Consulta un usuario por su identificador.

### Actualizar usuario

```http
PUT /users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json
```

Permite actualizar los datos del usuario, incluyendo su rol cuando se proporciona un `role_id` válido.

### Eliminar usuario

```http
DELETE /users/{user_id}
Authorization: Bearer <access_token>
```

Permite ejecutar la operación de eliminación de un usuario según las reglas del servicio.

Para consultar los esquemas completos, parámetros y respuestas de cada endpoint, utilizar Swagger UI.

## Respuestas HTTP

| Código | Descripción |
|---|---|
| 200 | Solicitud procesada correctamente. |
| 201 | Usuario creado correctamente. |
| 400 | Solicitud inválida o error de validación de negocio. |
| 401 | No autenticado o token inválido. |
| 404 | Usuario no encontrado. |
| 409 | Conflicto con un usuario o rol. |
| 500 | Error interno del servidor. |

## Ejecución local sin Docker

Para ejecutar el microservicio directamente en el equipo local:

### 1. Instalar dependencias

```powershell
uv sync
```

### 2. Configurar variables de entorno

Crear el archivo `.env` con las variables requeridas y ajustar las direcciones de PostgreSQL y del servicio de roles al entorno local.

### 3. Aplicar migraciones

```powershell
uv run alembic upgrade head
```

### 4. Iniciar FastAPI

```powershell
uv run uvicorn users.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

La ruta del módulo de inicio debe corresponder al punto de entrada configurado en el proyecto.

## Pruebas

El proyecto utiliza Pytest para validar los casos de uso y el comportamiento de los adaptadores.

Ejecutar todas las pruebas:

```powershell
uv run pytest
```

Las pruebas incluyen escenarios de gestión de usuarios, validación de datos, conflictos y asociación con roles.

## Calidad de código

El proyecto utiliza Ruff como herramienta de análisis estático y revisión de estilo.

Ejecutar el linter:

```powershell
uv run ruff check .
```

Corregir automáticamente los problemas que puedan resolverse:

```powershell
uv run ruff check . --fix
```

## Documentación de la API

FastAPI genera automáticamente la documentación interactiva:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI: `/openapi.json`

En Docker, las rutas están disponibles a través de `http://localhost:8001`.

## Estado del proyecto

Funcionalidades implementadas:

- Gestión de usuarios.
- Persistencia en PostgreSQL.
- Migraciones mediante Alembic.
- Integración con Auth0.
- Consulta del perfil autenticado.
- Asociación de usuarios con roles.
- Validación de roles mediante comunicación HTTP con `dialisis-roles`.
- Pruebas automatizadas con Pytest.
- Análisis estático con Ruff.
- Contenerización mediante Docker.
- Orquestación mediante Docker Compose.
- Integración con la base de datos compartida de Diálisis.