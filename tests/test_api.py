from fastapi.testclient import TestClient

import fastapi_app
from model.structured_data import SimplificationResponse, SimplificationText
from simplifier.core import ModelInvocationError

AUTH_HEADERS = {"Authorization": "Bearer test-api-token"}


class FakeSimplifier:
    def __init__(self) -> None:
        self.model: str | None = None
        self.received_text: str | None = None
        self.received_leichte_sprache: bool | None = None

    def set_model(self, value: str) -> None:
        self.model = value

    def simplify_text(self, text: str, leichte_sprache: bool = False) -> SimplificationResponse:
        self.received_text = text
        self.received_leichte_sprache = leichte_sprache
        return SimplificationResponse(simplifications=[SimplificationText(text="Straße")])


class FailingSimplifier(FakeSimplifier):
    def simplify_text(self, text: str, leichte_sprache: bool = False) -> SimplificationResponse:
        raise ModelInvocationError("OpenRouter request failed")


def client_with_simplifier(simplifier: FakeSimplifier) -> TestClient:
    fastapi_app.app.dependency_overrides[fastapi_app.get_simplifier] = lambda: simplifier
    return TestClient(fastapi_app.app)


def test_requires_bearer_token() -> None:
    client = client_with_simplifier(FakeSimplifier())

    response = client.post("/", json={"data": [{"text": "Ein Text."}]})

    assert response.status_code == 401


def test_rejects_models_outside_allowlist() -> None:
    client = client_with_simplifier(FakeSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": "Ein Text."}], "model": "expensive-model"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported model"


def test_rejects_total_input_text_over_limit() -> None:
    client = client_with_simplifier(FakeSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": "x" * 100_001}]},
    )

    assert response.status_code == 413


def test_simplifies_authorized_payload_and_postprocesses_sharp_s() -> None:
    simplifier = FakeSimplifier()
    client = client_with_simplifier(simplifier)

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={
            "data": [{"text": "Ein Text."}],
            "leichte_sprache": True,
            "model": "other-model",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"simplifications": [{"text": "Strasse"}]}
    assert simplifier.model == "other-model"
    assert simplifier.received_text == '[{"text": "Ein Text."}]'
    assert simplifier.received_leichte_sprache is True


def test_model_invocation_errors_become_bad_gateway() -> None:
    client = client_with_simplifier(FailingSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": "Ein Text."}]},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "Model provider request failed"


def test_cors_allows_configured_origin_without_wildcard() -> None:
    client = client_with_simplifier(FakeSimplifier())

    response = client.options(
        "/",
        headers={
            "Origin": "https://client.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://client.example"
    assert response.headers["access-control-allow-credentials"] == "true"
