from app.deidentification.rule_detector import detect_rule_entities


def test_detects_common_structured_identifiers_with_exact_spans():
    text = (
        "Email alice@example.org; SSN 123-45-6789; "
        "call (415) 555-0132; https://clinic.example/path. "
        "IP 192.0.2.10"
    )

    entities = detect_rule_entities(text)

    assert {
        (entity["label"], text[entity["start"]:entity["end"]])
        for entity in entities
    } == {
        ("EMAIL", "alice@example.org"),
        ("SSN", "123-45-6789"),
        ("PHONE", "(415) 555-0132"),
        ("URL", "https://clinic.example/path"),
        ("IP", "192.0.2.10"),
    }


def test_ignores_invalid_ipv4_and_numbers_embedded_in_longer_numbers():
    text = "Bad IP 999.1.1.1; reference 1234567890123."

    assert detect_rule_entities(text) == []
