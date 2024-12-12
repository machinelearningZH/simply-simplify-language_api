import pytest

from fastapi.testclient import TestClient
from fastapi_app import app, get_simplifier
from logger import logger

# Mock dependency function
def mock_get_simplifier():
    class MockSimplifier:
        def simplify_text(self, text, leichte_sprache):
            if leichte_sprache:
                return "The text simplified in leichte sprache"
            else:
                return "The text simplified in einfache sprache"

    return MockSimplifier()


json_example = {
    "data":  [
        {
            "text": "Hallo Welt"
        },
        {
            "text": "<p>Lorem ipsum dolor</p>"
        }
    ],
    "leichte_sprache": "False",
}

json_expected = {
    "data": [
        {
            "text": "Hallo Welt"
        }
    ],
    "leichte_sprache": "False",
}


# Fixture to override the dependency
@pytest.fixture
def client():
    app.dependency_overrides[get_simplifier] = mock_get_simplifier
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


def test_send_json(client):
    response = client.post(
        "/",
        json=json_example
    )
    assert response.status_code == 200
    assert response.json() == 'The text simplified in einfache sprache'


def test_send_text(client):
    response = client.post(
        "/",
        json=json_expected
    )
    assert response.status_code == 200
    assert response.json() == 'The text simplified in einfache sprache'


def test_send_nothing(client):
    response = client.post(
        "/",
        json={
            "data": "",
            "leichte_sprache": "True",
        }
    )
    assert response.status_code == 422
