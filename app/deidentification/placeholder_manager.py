import re


def assign_placeholders(text: str, entities: list[dict]) -> tuple[str, dict[str, str]]:
    ordered_entities = sorted(entities, key=lambda entity: entity["start"])
    mapping = {}
    placeholders_by_value = {}
    next_number_by_label = {}
    replacements = []

    for entity in ordered_entities:
        start = entity["start"]
        end = entity["end"]
        raw_label = entity.get("label")
        if not isinstance(raw_label, str) or not raw_label:
            raise ValueError(f"Entity is missing a label: {entity!r}")
        label = re.sub(r"[^A-Z0-9_]", "_", raw_label.upper())
        if not label or label[0].isdigit():
            label = f"ENTITY_{label}"
        if start < 0 or end <= start or end > len(text):
            raise ValueError(f"Entity span is outside the input text: {entity!r}")

        value = text[start:end]
        if entity.get("text", value) != value:
            raise ValueError(f"Entity text does not match its span: {entity!r}")
        if any(
            start < prior_end and prior_start < end
            for prior_start, prior_end, _ in replacements
        ):
            raise ValueError(f"Entity spans overlap: {entity!r}")

        key = (label, value)
        if key not in placeholders_by_value:
            number = next_number_by_label.get(label, 0) + 1
            placeholder = f"[{label}_{number}]"
            while placeholder in text or placeholder in mapping:
                number += 1
                placeholder = f"[{label}_{number}]"
            next_number_by_label[label] = number
            placeholders_by_value[key] = placeholder
            mapping[placeholder] = value
        replacements.append((start, end, placeholders_by_value[key]))

    masked_text = text
    for start, end, placeholder in reversed(replacements):
        masked_text = masked_text[:start] + placeholder + masked_text[end:]

    return masked_text, mapping
