import pytest

from logger import logger
from fastapi.testclient import TestClient
from fastapi_app import app, get_simplifier  # Assuming your FastAPI app is in a file named main.py


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
    "data": {
        "uuid": "1",
        "type": "section_title",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Hallo Welt"
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Lorem ipsum dolor</p>"
            }
        ],
    },
    "leichte_sprache": "False",
    "format": "json",
    "path": "fields[*].content",
    "root": "fields"
}

json_expected = {
    "uuid": "1",
    "type": "section_title",
    "fields": [
        {
            "name": "field_title",
            "type": "plaintext",
            "content": "Hallo Welt",
            "simplified_text": "Hallo Welt"
        },
        {
            "name": "field_lead",
            "type": "markup",
            "content": "<p>Lorem ipsum dolor</p>",
            "simplified_text": "<p>Lorem ipsum dolor</p>"
        }
    ],
    'simplification': 'einfache_sprache',
}

text_example = {
    "data": "Einfache Sprache",
    "leichte_sprache": "True",
    "format": "text"
}

text_expected = {
    "data": "Einfache Sprache",
    'simplification': 'einfache_sprache',
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
    assert response.json()["fields"][0]["simplified_text"] == 'The text simplified in einfache sprache'
    assert response.json()["simplification"] == 'einfache_sprache'


def test_send_text(client):
    response = client.post(
        "/",
        json=text_example
    )
    assert response.status_code == 200
    assert response.json()["data"] == 'The text simplified in leichte sprache'
    assert response.json()["simplification"] == 'leichte_sprache'


def test_send_nothing(client):
    response = client.post(
        "/",
        json={
            "data": "",
            "leichte_sprache": "True",
            "format": "text"
        }
    )
    assert response.status_code == 200
    # Testing only the simplification as we can't really predict what OpenAI is going to give us as an answer
    assert response.json()["simplification"] == 'leichte_sprache'
