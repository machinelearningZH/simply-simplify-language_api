from typing import Any

import pytest
from pydantic import ValidationError

from config import load_settings
from model.structured_data import SimplificationResponse
from simplifier.core import ModelResponseError, Simplifier


class InvalidResponseCompletions:
    def parse(self, **kwargs: Any) -> None:
        try:
            SimplificationResponse.model_validate({"simplifications": []})
        except ValidationError as exc:
            raise exc
        raise AssertionError("Expected response validation to fail")


class FakeChat:
    completions = InvalidResponseCompletions()


class FakeBeta:
    chat = FakeChat()


class InvalidResponseClient:
    beta = FakeBeta()


def test_invalid_structured_response_becomes_model_response_error() -> None:
    simplifier = Simplifier(
        settings=load_settings(load_env_file=False),
        client=InvalidResponseClient(),  # type: ignore[arg-type]
    )

    with pytest.raises(ModelResponseError, match="expected schema"):
        simplifier.simplify_text('[{"text": "Ein Text."}]')
