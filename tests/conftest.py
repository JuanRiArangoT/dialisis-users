import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from users.adapters.inbound.http.dependencies.auth0_jwt import get_current_user
from users.main import app


@pytest.fixture
def authenticated_user():
    def set_authenticated_user(
        auth0_user_id: str,
        email: str = "test@dialisis.test",
    ):
        def override():
            return {
                "sub": auth0_user_id,
                "email": email,
            }

        app.dependency_overrides[get_current_user] = override

    yield set_authenticated_user

    app.dependency_overrides.pop(get_current_user, None)