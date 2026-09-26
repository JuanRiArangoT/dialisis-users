from uuid import uuid4

from fastapi.testclient import TestClient

from users.adapters.inbound.http.dependencies.auth0_jwt import get_current_user
from users.main import app


def mock_current_user() -> dict:
    return {
        "sub": "auth0|test-user",
        "email": "test@dialisis.test",
    }


app.dependency_overrides[get_current_user] = mock_current_user

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "auth0_user_id": f"auth0|test-{uuid4()}",
            "email": f"test-{uuid4()}@dialisis.test",
            "full_name": "Usuario de Prueba",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "user_id" in data
    assert data["full_name"] == "Usuario de Prueba"
    assert data["tipo_documento"] == "CC"
    assert data["is_active"] is True


def test_get_user(authenticated_user):
    auth0_user_id = f"auth0|test-{uuid4()}"
    email = f"test-{uuid4()}@dialisis.test"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": auth0_user_id,
            "email": email,
            "full_name": "Usuario GET",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(auth0_user_id, email)

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["auth0_user_id"] == auth0_user_id
    assert data["email"] == email
    assert data["full_name"] == "Usuario GET"

def test_update_user(authenticated_user):
    auth0_user_id = f"auth0|test-{uuid4()}"
    email = f"test-{uuid4()}@dialisis.test"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": auth0_user_id,
            "email": email,
            "full_name": "Usuario Original",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(auth0_user_id, email)

    response = client.put(
        f"/users/{user_id}",
        json={
            "email": email,
            "full_name": "Usuario Actualizado",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
            "is_active": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["email"] == email
    assert data["full_name"] == "Usuario Actualizado"
    assert data["is_active"] is True

def test_delete_user(authenticated_user):
    auth0_user_id = f"auth0|test-{uuid4()}"
    email = f"test-{uuid4()}@dialisis.test"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": auth0_user_id,
            "email": email,
            "full_name": "Usuario a Eliminar",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(auth0_user_id, email)

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204

def test_get_user_not_found(authenticated_user):
    authenticated_user("auth0|test-user")
    user_id = str(uuid4())

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_duplicate_email():
    email = f"duplicate-{uuid4()}@dialisis.test"

    first_response = client.post(
        "/users",
        json={
            "auth0_user_id": f"auth0|test-{uuid4()}",
            "email": email,
            "full_name": "Primer Usuario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users",
        json={
            "auth0_user_id": f"auth0|test-{uuid4()}",
            "email": email,
            "full_name": "Segundo Usuario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A user with this email already exists."
    }

def test_create_user_duplicate_auth0_id():
    auth0_user_id = f"auth0|duplicate-{uuid4()}"

    first_response = client.post(
        "/users",
        json={
            "auth0_user_id": auth0_user_id,
            "email": f"first-{uuid4()}@dialisis.test",
            "full_name": "Primer Usuario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users",
        json={
            "auth0_user_id": auth0_user_id,
            "email": f"second-{uuid4()}@dialisis.test",
            "full_name": "Segundo Usuario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A user with this Auth0 ID already exists."
    }

def test_create_user_duplicate_document():
    numero_documento = str(uuid4().int)[:10]

    first_response = client.post(
        "/users",
        json={
            "auth0_user_id": f"auth0|first-{uuid4()}",
            "email": f"first-{uuid4()}@dialisis.test",
            "full_name": "Primer Usuario",
            "tipo_documento": "CC",
            "numero_documento": numero_documento,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users",
        json={
            "auth0_user_id": f"auth0|second-{uuid4()}",
            "email": f"second-{uuid4()}@dialisis.test",
            "full_name": "Segundo Usuario",
            "tipo_documento": "CC",
            "numero_documento": numero_documento,
        },
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A user with this document number already exists."
    }


def test_get_user_forbidden_for_different_authenticated_user(authenticated_user):
    owner_auth0_user_id = f"auth0|owner-{uuid4()}"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": owner_auth0_user_id,
            "email": f"owner-{uuid4()}@dialisis.test",
            "full_name": "Usuario Propietario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(
        "auth0|otro-usuario",
        "otro@dialisis.test",
    )

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user_forbidden_for_different_authenticated_user(
    authenticated_user,
):
    owner_auth0_user_id = f"auth0|owner-{uuid4()}"
    owner_email = f"owner-{uuid4()}@dialisis.test"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": owner_auth0_user_id,
            "email": owner_email,
            "full_name": "Usuario Propietario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(
        "auth0|otro-usuario",
        "otro@dialisis.test",
    )

    response = client.put(
        f"/users/{user_id}",
        json={
            "email": owner_email,
            "full_name": "Usuario Modificado",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
            "is_active": True,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_delete_user_forbidden_for_different_authenticated_user(
    authenticated_user,
):
    owner_auth0_user_id = f"auth0|owner-{uuid4()}"

    create_response = client.post(
        "/users",
        json={
            "auth0_user_id": owner_auth0_user_id,
            "email": f"owner-{uuid4()}@dialisis.test",
            "full_name": "Usuario Propietario",
            "tipo_documento": "CC",
            "numero_documento": str(uuid4().int)[:10],
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["user_id"]

    authenticated_user(
        "auth0|otro-usuario",
        "otro@dialisis.test",
    )

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}