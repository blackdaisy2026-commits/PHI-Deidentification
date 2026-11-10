import pytest

from app.deidentification.placeholder_manager import assign_placeholders
from app.deidentification.span_merger import merge_spans


def test_merge_keeps_longest_overlapping_span_and_orders_results():
    entities = [
        {"start": 10, "end": 18, "label": "LONGER"},
        {"start": 2, "end": 8, "label": "LONG"},
        {"start": 12, "end": 18, "label": "OVERLAP"},
    ]

    assert merge_spans(entities) == [
        {"start": 2, "end": 8, "label": "LONG"},
        {"start": 10, "end": 18, "label": "LONGER"},
    ]


def test_merge_rejects_invalid_spans():
    with pytest.raises(ValueError, match="Invalid entity span"):
        merge_spans([{"start": 3, "end": 3, "label": "NAME"}])


def test_placeholder_assignment_reuses_same_value_and_avoids_input_collision():
    text = (
        "Send person@example.org to [EMAIL_1] and [EMAIL_2]; "
        "resend to person@example.org."
    )
    first_start = text.index("person@example.org")
    second_start = text.rindex("person@example.org")
    entities = [
        {
            "start": first_start,
            "end": first_start + len("person@example.org"),
            "text": "person@example.org",
            "label": "EMAIL",
        },
        {
            "start": second_start,
            "end": second_start + len("person@example.org"),
            "text": "person@example.org",
            "label": "EMAIL",
        }
    ]

    masked, mapping = assign_placeholders(text, entities)

    assert masked.count("[EMAIL_3]") == 2
    assert mapping == {"[EMAIL_3]": "person@example.org"}


def test_placeholder_assignment_rejects_stale_entity_text():
    with pytest.raises(ValueError, match="does not match"):
        assign_placeholders(
            "Alice",
            [{"start": 0, "end": 5, "text": "Bob", "label": "NAME"}],
        )
