from converter.TextConverter import TextConverter
from model.TextPayload import TextPayload

payload = {
    "data": "Fames integer pésuéré egéstapérès aenean aptent senectus meturaé pulvinar juséo, ultrûcéas férmentum facilisis sodales volupque, et péer fuegiuia dui.",
    "leichte_sprache": "False",
    "format": "text"
}

json = TextPayload(**payload)


def mock_get_simplifier():
    class MockSimplifier:
        def simplify_text(self, text, leichte_sprache):
            if leichte_sprache:
                return "The text simplified in leichte sprache"
            else:
                return "The text simplified in einfache sprache"

    return MockSimplifier()


def test_should_extract_values_from_text():
    # Create a TextConverter
    converter = TextConverter(json, mock_get_simplifier())
    result = converter.simplify()

    # Test the sprache is correctly set
    assert converter.sprache == 'einfache_sprache'

    assert result["simplification"] == "einfache_sprache"
