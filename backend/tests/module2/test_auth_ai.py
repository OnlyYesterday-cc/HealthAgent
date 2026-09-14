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
        pytest.param("access", None, False, id="M2-TC-006"),
        pytest.param("access", str(2**63), False, id="M2-TC-007"),
        pytest.param("refresh", str(2**63), False, id="M2-TC-008"),
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


def register_headers(http):
    response = http.post('/api/v1/auth/register', json={
        'username': 'module2_user', 'email': 'module2@example.com', 'password': 'secret123',
    })
    assert response.status_code == 201, response.text
    return {'Authorization': 'Bearer ' + response.json()['tokens']['access_token']}


@pytest.mark.parametrize('nickname', ['N' * 64], ids=['M2-TC-009'])
def test_nickname_length_boundary_preserves_previous_value(http, nickname):
    headers = register_headers(http)
    response = http.patch('/api/v1/users/me', headers=headers, json={'nickname': nickname})
    assert response.status_code == 200, response.text
    assert response.json()['nickname'] == nickname
    rejected = http.patch('/api/v1/users/me', headers=headers, json={'nickname': nickname + 'X'})
    assert rejected.status_code == 422, rejected.text
    current = http.get('/api/v1/users/me', headers=headers)
    assert current.status_code == 200, current.text
    assert current.json()['nickname'] == nickname


@pytest.mark.parametrize('nickname', ['\u6c49' * 64], ids=['M2-TC-010'])
def test_unicode_nickname_boundary_and_clear(http, nickname):
    headers = register_headers(http)
    response = http.patch('/api/v1/users/me', headers=headers, json={'nickname': nickname})
    assert response.status_code == 200, response.text
    assert response.json()['nickname'] == nickname
    rejected = http.patch('/api/v1/users/me', headers=headers, json={'nickname': nickname + '\u6c49'})
    assert rejected.status_code == 422, rejected.text
    cleared = http.patch('/api/v1/users/me', headers=headers, json={'nickname': None})
    assert cleared.status_code == 200, cleared.text
    current = http.get('/api/v1/users/me', headers=headers)
    assert current.status_code == 200, current.text
    assert current.json()['nickname'] is None
