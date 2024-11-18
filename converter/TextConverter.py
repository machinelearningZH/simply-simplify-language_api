from jsonpath_ng import parse
from simplifier.core import simplify_text


class TextConverter:

    def __init__(self, text: str, leichte_sprache: bool = False, path: str = 'simplified_text') -> None:
        self.text = text
        self.path = path
        self.is_leichte_sprache = leichte_sprache
        self.sprache = 'leichte_sprache' if leichte_sprache else 'einfache_sprache'

    def simplify(self):
        simplified_text = simplify_text(self.text, self.is_leichte_sprache)
        return {
            self.path: simplified_text,
            "simplification": self.sprache
        }
