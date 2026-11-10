def merge_spans(entities: list[dict]) -> list[dict]:
    candidates = []
    for entity in entities:
        start = entity.get("start")
        end = entity.get("end")
        if (
            not isinstance(start, int)
            or isinstance(start, bool)
            or not isinstance(end, int)
            or isinstance(end, bool)
            or start < 0
            or end <= start
        ):
            raise ValueError(f"Invalid entity span: {entity!r}")
        if not isinstance(entity.get("label"), str) or not entity["label"]:
            raise ValueError(f"Entity is missing a label: {entity!r}")
        candidates.append(entity)

    candidates.sort(
        key=lambda entity: (
            -(entity["end"] - entity["start"]),
            entity["start"],
            entity["label"],
        )
    )
    selected = []
    for candidate in candidates:
        if any(
            candidate["start"] < existing["end"]
            and existing["start"] < candidate["end"]
            for existing in selected
        ):
            continue
        selected.append(candidate)

    return sorted(selected, key=lambda entity: (entity["start"], entity["end"]))
