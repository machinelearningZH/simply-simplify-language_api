from jsonpath_ng import parse
from converter.BadFormattingError import BadFormattingError


class JsonConverter:

    def __init__(self, payload, simplifier, model: str = None) -> None:

        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.json = payload.data
        self.path = payload.path
        self.root = payload.root
        self.is_leichte_sprache = bool(payload.leichte_sprache)
        self.sprache = 'leichte_sprache' if self.is_leichte_sprache else 'einfache_sprache'
        self.data = []

    def extract_from_payload(self):
        expression = parse(self.path)

        # Extract values
        self.data = [match.value for match in expression.find(self.json)]

        if len(self.data) > 0:
            return self.data
        else:
            raise BadFormattingError(500)

    def add_to_payload(self, data):
        json = self.json[self.root] if self.root else self.json
        if self.root:
            for index, field in enumerate(json):
                field["simplified_text"] = data[index]
        else:
            json["simplified_text"] = data

        self.json["simplification"] = self.sprache

        return self.json

    def convert(self):
        values = self.extract_from_payload()
        # Pass through the simplifier
        for index, value in enumerate(values):
            values[index] = self.simplifier.simplify_text(value, self.is_leichte_sprache)

        return values

    def simplify(self):
        converted = self.convert()

        return self.add_to_payload(converted)
