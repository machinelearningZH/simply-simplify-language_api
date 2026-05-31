import json

from model.structured_data import SimplificationResponse


class DataConverter:
    def __init__(self, payload, simplifier, model: str | None = None) -> None:
        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.input_text = json.dumps(
            [item.model_dump() for item in payload.data],
            ensure_ascii=False,
        )
        self.leichte_sprache = payload.leichte_sprache is True

    def simplify(self) -> SimplificationResponse:
        results = self.simplifier.simplify_text(self.input_text, self.leichte_sprache)

        data = results.model_dump()

        for item in data["simplifications"]:
            item["text"] = item["text"].replace("ß", "ss")

        return SimplificationResponse.model_validate(data)
