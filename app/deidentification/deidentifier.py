from .placeholder_manager import assign_placeholders
from .rule_detector import detect_rule_entities
from .span_merger import merge_spans


def deidentify(text: str) -> tuple[str, dict[str, str]]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    entities = merge_spans(detect_rule_entities(text))
    return assign_placeholders(text, entities)
