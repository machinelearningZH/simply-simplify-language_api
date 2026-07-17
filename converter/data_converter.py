import json

from model.structured_data import Payload, SimplificationResponse
from simplifier.core import ModelResponseError, Simplifier


class DataConverter:
    def __init__(self, payload: Payload, simplifier: Simplifier, model: str) -> None:
        self.simplifier = simplifier
        self.model = model
        self.expected_result_count = len(payload.data)
        self.input_text = json.dumps(
            [item.model_dump() for item in payload.data],
            ensure_ascii=False,
        )
        self.leichte_sprache = payload.leichte_sprache is True

    def simplify(self) -> SimplificationResponse:
        results = self.simplifier.simplify_text(
            self.input_text,
            self.leichte_sprache,
            self.model,
        )
        if len(results.simplifications) != self.expected_result_count:
            raise ModelResponseError(
                "Model response item count did not match the request item count"
            )
        return results
