from uuid import uuid4

from fastapi.testclient import TestClient

from users.main import app

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


def test_get_user():
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

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["auth0_user_id"] == auth0_user_id
    assert data["email"] == email
    assert data["full_name"] == "Usuario GET"