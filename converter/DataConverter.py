class DataConverter:

    def __init__(self, payload, simplifier, model: str = None) -> None:
        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.json = payload.data
        self.leichte_sprache = bool(payload.leichte_sprache)

    def simplify(self):
        return self.simplifier.simplify_text(self.json, self.leichte_sprache)
