"""M1-D02 and M1-D03 regression checks, separate from the 15-case batch."""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['JWT_SECRET'] = 'isolated-defect-regression-only'
os.environ['APP_DEBUG'] = 'false'
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'backend'))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import create_app


@pytest.fixture
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    app = create_app()

    def database():
        with sessions() as session:
            yield session

    app.dependency_overrides[get_db] = database
    http = TestClient(app, raise_server_exceptions=False)
    try:
        yield http
    finally:
        http.close()
        app.dependency_overrides.clear()
        engine.dispose()


def register(client, username='regression_user', password='secret123'):
    response = client.post('/api/v1/auth/register', json={
        'username': username, 'email': username + '@example.com', 'password': password,
    })
    assert response.status_code == 201, response.text
    return {'Authorization': 'Bearer ' + response.json()['tokens']['access_token']}




def create_record(client, headers):
    response = client.post('/api/v1/bp-records', headers=headers, json={
        'systolic': 120, 'diastolic': 80, 'heart_rate': 72,
        'measured_at': '2026-09-12T08:00:00+08:00', 'note': 'original',
    })
    assert response.status_code == 201, response.text
    return response.json()




def test_m1_d02_required_null_rejected_nullable_fields_clearable(client):
    headers = register(client)
    original = create_record(client, headers)
    endpoint = f"/api/v1/bp-records/{original['id']}"
    for field in ['systolic', 'diastolic', 'measured_at']:
        response = client.patch(endpoint, headers=headers, json={field: None})
        assert response.status_code == 422, response.text
        current = client.get(endpoint, headers=headers)
        assert current.status_code == 200
        assert current.json()[field] == original[field]
    response = client.patch(endpoint, headers=headers, json={'note': 'updated'})
    assert response.status_code == 200
    assert response.json()['systolic'] == 120
    assert response.json()['note'] == 'updated'
    response = client.patch(endpoint, headers=headers, json={'heart_rate': None, 'note': None})
    assert response.status_code == 200
    assert response.json()['heart_rate'] is None and response.json()['note'] is None


def test_m1_d03_timezone_equivalence_create_update_and_query(client):
    headers = register(client)
    created = create_record(client, headers)
    ranges = [
        ('2026-09-12T00:00:00Z', '2026-09-12T00:00:01Z'),
        ('2026-09-12T08:00:00+08:00', '2026-09-12T08:00:01+08:00'),
        ('2026-09-11T19:00:00-05:00', '2026-09-11T19:00:01-05:00'),
    ]
    for start, end in ranges:
        response = client.get('/api/v1/bp-records', headers=headers, params={'start': start, 'end': end})
        assert response.status_code == 200
        assert response.json()['total'] == 1, response.text
        assert response.json()['items'][0]['id'] == created['id']
    parsed = datetime.fromisoformat(created['measured_at'].replace('Z', '+00:00'))
    assert parsed.tzinfo is not None
    assert parsed == datetime(2026, 9, 12, tzinfo=timezone.utc)
    endpoint = f"/api/v1/bp-records/{created['id']}"
    updated = client.patch(endpoint, headers=headers, json={'measured_at': '2026-09-13T05:30:00+05:30'})
    assert updated.status_code == 200
    response = client.get('/api/v1/bp-records', headers=headers, params={
        'start': '2026-09-13T00:00:00Z', 'end': '2026-09-13T00:00:01Z',
    })
    assert response.json()['total'] == 1
    # Existing API accepts naive datetimes; explicitly retain UTC interpretation.
    updated = client.patch(endpoint, headers=headers, json={'measured_at': '2026-09-14T00:00:00'})
    assert updated.status_code == 200
    response = client.get('/api/v1/bp-records', headers=headers, params={
        'start': '2026-09-14T00:00:00Z', 'end': '2026-09-14T00:00:01Z',
    })
    assert response.json()['total'] == 1
