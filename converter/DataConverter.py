class DataConverter:

    def __init__(self, payload, simplifier, model: str = None) -> None:

        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.json = payload.data
        self.is_leichte_sprache = bool(payload.leichte_sprache)
        self.sprache = 'leichte_sprache' if self.is_leichte_sprache else 'einfache_sprache'
        self.data = []

    def convert(self):
        return self.simplifier.simplify_text(self.json, self.is_leichte_sprache)

    def simplify(self):
        return self.convert()