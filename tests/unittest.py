from converter.JsonConverter import JsonConverter
from converter.TextConverter import TextConverter


def test_should_extract_values_01():

    json_example = {
        "contents": [
            {"text": "Hello World 2"},
            {"text": "<p>Lorem ipsum dolor amet</p>"}
        ]
    }

    schema = "contents[*].text"

    # Create a JsonConverter with the schema we want, to find the content in the JSON
    # Root is the path to which we append back the simplified text
    converter = JsonConverter(json_example, schema, "contents", False)
    values = converter.extract_from_payload()

    # Test that the correct values are extracted form the JSON
    assert values == ["Hello World 2", "<p>Lorem ipsum dolor amet</p>"]


def test_should_extract_values_02():
    json_example = [
        {"text": "Hello World 2"},
        {"text": "<p>Lorem ipsum dolor amet</p>"}
    ]

    schema = "$[*].text"

    # Create a JsonConverter with the schema we want, to find the content in the JSON
    # Root is the path to which we append back the simplified text
    converter = JsonConverter(json_example, schema, "", False)
    values = converter.extract_from_payload()

    # Test that the correct values are extracted form the JSON
    assert values == ["Hello World 2", "<p>Lorem ipsum dolor amet</p>"]