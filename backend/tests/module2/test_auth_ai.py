"""AI-assisted module-two cases; signed malformed tokens are test fixtures."""
import time

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import get_settings


@pytest.fixture
def http(client):
    # Observe the actual HTTP response instead of propagating server exceptions.
    session = TestClient(client.app, raise_server_exceptions=False)
    try:
        yield session
    finally:
        session.close()


@pytest.mark.parametrize(
    "token_type,subject,expired",
    [
        pytest.param("access", "not-an-integer", False, id="M2-TC-001"),
        pytest.param("refresh", "not-an-integer", False, id="M2-TC-002"),
        pytest.param("refresh", None, False, id="M2-TC-003"),
        pytest.param("access", "1", True, id="M2-TC-004"),
        pytest.param("refresh", "1", True, id="M2-TC-005"),
    ],
)
def test_invalid_credentials_return_401(http, token_type, subject, expired):
    settings = get_settings()
    now = int(time.time())
    claims = {"type": token_type, "iat": now - 120, "exp": now - 60 if expired else now + 300}
    if subject is not None:
        claims["sub"] = subject
    token = jwt.encode(claims, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    if token_type == "access":
        response = http.get("/api/v1/users/me", headers={"Authorization": "Bearer " + token})
    else:
        response = http.post("/api/v1/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 401, response.text
    assert "access_token" not in response.json()
