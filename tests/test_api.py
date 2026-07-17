from fastapi.testclient import TestClient

import fastapi_app
from model.structured_data import SimplificationResponse, SimplificationText
from simplifier.core import ModelInvocationError

AUTH_HEADERS = {"Authorization": "Bearer test-api-token"}


class FakeSimplifier:
    def __init__(self) -> None:
        self.closed = False
        self.model: str | None = None
        self.received_text: str | None = None
        self.received_leichte_sprache: bool | None = None

    def simplify_text(
        self,
        text: str,
        leichte_sprache: bool = False,
        model: str | None = None,
    ) -> SimplificationResponse:
        self.model = model
        self.received_text = text
        self.received_leichte_sprache = leichte_sprache
        return SimplificationResponse(simplifications=[SimplificationText(text="Strasse")])

    def close(self) -> None:
        self.closed = True


class FailingSimplifier(FakeSimplifier):
    def simplify_text(
        self,
        text: str,
        leichte_sprache: bool = False,
        model: str | None = None,
    ) -> SimplificationResponse:
        raise ModelInvocationError("OpenRouter request failed")


class MismatchedSimplifier(FakeSimplifier):
    def simplify_text(
        self,
        text: str,
        leichte_sprache: bool = False,
        model: str | None = None,
    ) -> SimplificationResponse:
        return SimplificationResponse(
            simplifications=[
                SimplificationText(text="Erster Text."),
                SimplificationText(text="Unerwarteter zweiter Text."),
            ]
        )


class HtmlSimplifier(FakeSimplifier):
    def simplify_text(
        self,
        text: str,
        leichte_sprache: bool = False,
        model: str | None = None,
    ) -> SimplificationResponse:
        return SimplificationResponse(
            simplifications=[SimplificationText(text='<a href="/straße">Strasse</a>')]
        )


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


def test_simplifies_authorized_payload_with_selected_model() -> None:
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


def test_preserves_html_attributes_exactly() -> None:
    client = client_with_simplifier(HtmlSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": '<a href="/straße">Straße</a>'}]},
    )

    assert response.status_code == 200
    assert response.json() == {"simplifications": [{"text": '<a href="/straße">Strasse</a>'}]}


def test_rejects_model_response_with_wrong_item_count() -> None:
    client = client_with_simplifier(MismatchedSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": "Ein Text."}]},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "Model provider response was invalid"


def test_rejects_whitespace_only_text() -> None:
    client = client_with_simplifier(FakeSimplifier())

    response = client.post(
        "/",
        headers=AUTH_HEADERS,
        json={"data": [{"text": "   "}]},
    )

    assert response.status_code == 422


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
    assert "access-control-allow-credentials" not in response.headers


def test_lifespan_reuses_and_closes_simplifier(monkeypatch) -> None:
    simplifier = FakeSimplifier()
    monkeypatch.setattr(fastapi_app, "Simplifier", lambda settings: simplifier)

    with TestClient(fastapi_app.app) as client:
        response = client.post(
            "/",
            headers=AUTH_HEADERS,
            json={"data": [{"text": "Ein Text."}]},
        )
        assert response.status_code == 200
        assert fastapi_app.app.state.simplifier is simplifier
        assert simplifier.closed is False

    assert simplifier.closed is True
