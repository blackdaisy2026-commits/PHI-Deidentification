import pytest

from app.deidentification.deidentifier import deidentify
from app.deidentification.rehydrator import rehydrate


def test_deidentify_masks_identifiers_and_rehydrates_only_from_local_mapping():
    note = "Contact Alex at alex@example.org or (415) 555-0132."

    masked, mapping = deidentify(note)

    assert masked == "Contact Alex at [EMAIL_1] or [PHONE_1]."
    assert mapping == {
        "[EMAIL_1]": "alex@example.org",
        "[PHONE_1]": "(415) 555-0132",
    }
    assert rehydrate(masked, mapping) == note


def test_deidentify_accepts_empty_text_and_rejects_non_string_input():
    assert deidentify("") == ("", {})

    with pytest.raises(TypeError, match="text must be a string"):
        deidentify(None)
