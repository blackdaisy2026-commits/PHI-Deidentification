from app.deidentification.rehydrator import rehydrate


def test_restores_only_known_placeholders():
    response = "Hello [NAME_1]; keep [NAME_2] unresolved."

    assert rehydrate(response, {"[NAME_1]": "Alex"}) == (
        "Hello Alex; keep [NAME_2] unresolved."
    )
