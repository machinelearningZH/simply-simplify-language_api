from converter.TextConverter import TextConverter

text = ("Fames integer pésuéré egéstat vestibulum. Vivamus lacinia sociosqu pérès aenean aptent senectus metus "
        "umst phaséllœs gravida. Ultrices nullä malesuada aptenté pulvinar juséo, ultrûcéas férmentum facilisis "
        "sodales voluptà scelerisque, et péer fuegiuia dui. ")


def test_should_extract_values_from_text():

    # Create a TextConverter
    converter = TextConverter(text, False, "translated")
    result = converter.simplify()

    # Test the sprache is correctly set
    assert converter.sprache == 'einfache_sprache'

    assert result["simplification"] == "einfache_sprache"
