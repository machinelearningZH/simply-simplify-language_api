from model.TextPayload import TextPayload
from converter.JsonConverter import JsonConverter

json_example1 = {
    "data": {
        "uuid": "1",
        "type": "section_title",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Hello World"
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Lorem ipsum dolor</p>"
            }
        ],
    },
    "leichte_sprache": "False",
    "format": "json",
    "path": "fields[*].content",
    "root": "fields"
}

json_example2 = {
    "data": {
        "uuid": "1",
        "type": "section_title",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Hello World"
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Lorem ipsum dolor</p>"
            }
        ],
    },
    "leichte_sprache": "True",
    "format": "json",
    "path": "fields[*].content",
    "root": ""
}

json1 = TextPayload(**json_example1)
json2 = TextPayload(**json_example2)


def mock_get_simplifier():
    class MockSimplifier:
        def simplify_text(self, text, leichte_sprache):
            if leichte_sprache:
                return "The text simplified in leichte sprache"
            else:
                return "The text simplified in einfache sprache"

    return MockSimplifier()


def test_should_extract_values_from_json_with_root():
    # Create a JsonConverter with the schema we want, to find the content in the JSON
    # Root is the path to which we append back the simplified text
    converter = JsonConverter(json1, mock_get_simplifier())
    values = converter.extract_from_payload()

    # Test that the correct values are extracted form the JSON
    assert values == ["Hello World", "<p>Lorem ipsum dolor</p>"]

    # Add to payload back the correct position
    results = converter.add_to_payload(["TEST Hello World", "<p>TEST Lorem ipsum dolor</p>"])

    expected = {
        "uuid": "1",
        "type": "section_title",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Hello World",
                "simplified_text": "TEST Hello World"
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Lorem ipsum dolor</p>",
                "simplified_text": "<p>TEST Lorem ipsum dolor</p>"
            }
        ],
        'simplification': 'einfache_sprache',
    }

    assert results == expected

    # Test the sprache is correctly set
    assert converter.sprache == 'einfache_sprache'


def test_should_extract_values_from_json_without_root():
    # Create a JsonConverter with the schema we want, to find the content in the JSON
    # Root is the path to which we append back the simplified text
    converter = JsonConverter(json2, mock_get_simplifier())
    values = converter.extract_from_payload()

    # Test that the correct values are extracted form the JSON
    assert values == ["Hello World", "<p>Lorem ipsum dolor</p>"]

    # Add to payload back the correct position
    results = converter.add_to_payload(["TEST Hello World", "<p>TEST Lorem ipsum dolor</p>"])

    expected = {
        "uuid": "1",
        "type": "section_title",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Hello World",
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Lorem ipsum dolor</p>",
            }
        ],
        "simplification": "leichte_sprache",
        "simplified_text": [
            "TEST Hello World",
            "<p>TEST Lorem ipsum dolor</p>"
        ]
    }

    assert results == expected

    # Test the sprache is correctly set
    assert converter.sprache == 'leichte_sprache'
