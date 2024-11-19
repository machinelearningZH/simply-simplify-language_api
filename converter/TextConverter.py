class TextConverter:

    def __init__(self, payload, simplifier, model: str = None) -> None:
        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.text = payload.data
        self.path = payload.path if payload.path else "data"
        self.is_leichte_sprache = bool(payload.leichte_sprache)
        self.sprache = 'leichte_sprache' if self.is_leichte_sprache else 'einfache_sprache'

    def simplify(self):
        simplified_text = self.simplifier.simplify_text(self.text, self.is_leichte_sprache)
        return {
            self.path: simplified_text,
            "simplification": self.sprache
        }
