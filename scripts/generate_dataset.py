import argparse
import json
import random
import string
from datetime import date, timedelta
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = PROJECT_ROOT / "data" / "synthetic"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
_PHONE_AREA_CODES = {
    "train": tuple(range(201, 216)),
    "validation": tuple(range(301, 316)),
    "gold": tuple(range(401, 416)),
}
_CONDITIONS = (
    "asthma",
    "hypertension",
    "migraine",
    "type 2 diabetes",
    "seasonal allergies",
)
_FIRST_NAMES = (
    "Alex", "Avery", "Bailey", "Casey", "Cameron", "Dakota", "Drew", "Elliot",
    "Emerson", "Finley", "Harper", "Jamie", "Jordan", "Kai", "Logan", "Morgan",
    "Parker", "Quinn", "Riley", "Robin", "Rowan", "Sam", "Taylor", "Terry",
)
_LAST_NAMES = (
    "Example", "Sample", "Fiction", "Demo", "Test", "Mock", "Imaginary",
    "Placeholder", "Synthetic", "Simulated", "Generated", "Invented",
    "Fable", "Model", "Practice", "Training", "Pseudonym", "Artificial",
)


class _NoteBuilder:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.entities: list[dict[str, Any]] = []
        self.length = 0

    def add_text(self, text: str) -> None:
        self.parts.append(text)
        self.length += len(text)

    def add_entity(self, text: str, label: str) -> None:
        start = self.length
        self.add_text(text)
        self.entities.append(
            {"start": start, "end": self.length, "text": text, "label": label}
        )

    def build(self) -> tuple[str, list[dict[str, Any]]]:
        return "".join(self.parts), self.entities


def _phone_number(split: str, index: int) -> str:
    area_codes = _PHONE_AREA_CODES[split]
    area_code_index, suffix = divmod(index, 100)
    if area_code_index >= len(area_codes):
        capacity = len(area_codes) * 100
        raise ValueError(
            f"{split} supports at most {capacity} unique synthetic phone numbers"
        )
    return f"+1 ({area_codes[area_code_index]}) 555-01{suffix:02d}"


def _make_record(
    split: str,
    index: int,
    rng: random.Random,
    used_names: set[str],
    include_entities: bool,
) -> dict[str, Any]:
    name = _unique_synthetic_name(rng, used_names)
    age = rng.randint(18, 99)
    visit_date = date(2025, 12, 31) - timedelta(days=rng.randrange(365 * 30))
    date_text = visit_date.strftime("%m/%d/%Y")
    medical_record_number = f"SYN-{split[:3].upper()}-{index + 1:06d}"
    phone = _phone_number(split, index)
    email = f"patient.{split}.{index + 1:06d}@example.test"
    address = (
        f"{rng.randint(1, 999)} Example Road, Fictional City, "
        f"ZZ 00000"
    )
    condition = rng.choice(_CONDITIONS)

    builder = _NoteBuilder()
    if rng.choice((True, False)):
        builder.add_text("Follow-up visit: ")
        builder.add_entity(name, "NAME")
        builder.add_text(", age ")
        if age > 89:
            builder.add_entity(str(age), "AGE")
        else:
            builder.add_text(str(age))
        builder.add_text(" years, on ")
        builder.add_entity(date_text[:5], "DATE")
        builder.add_text(date_text[5:])
        builder.add_text(f" for {condition}. MRN: ")
        builder.add_entity(medical_record_number, "MRN")
        builder.add_text(". Contact ")
        builder.add_entity(phone, "PHONE")
        builder.add_text(" / ")
        builder.add_entity(email, "EMAIL")
        builder.add_text(". Address: ")
        builder.add_entity(address, "LOCATION")
        builder.add_text(".")
    else:
        builder.add_text("Patient ")
        builder.add_entity(name, "NAME")
        builder.add_text(", age ")
        if age > 89:
            builder.add_entity(str(age), "AGE")
        else:
            builder.add_text(str(age))
        builder.add_text(f", was evaluated for {condition} on ")
        builder.add_entity(date_text[:5], "DATE")
        builder.add_text(date_text[5:])
        builder.add_text(". Contact: ")
        builder.add_entity(email, "EMAIL")
        builder.add_text(", ")
        builder.add_entity(phone, "PHONE")
        builder.add_text(". Record ID ")
        builder.add_entity(medical_record_number, "MRN")
        builder.add_text(". Residence: ")
        builder.add_entity(address, "LOCATION")
        builder.add_text(".")

    text, entities = builder.build()
    record = {"id": f"{split}-{index + 1:06d}", "text": text}
    if include_entities:
        record["entities"] = entities
    return record


def _unique_synthetic_name(rng: random.Random, used_names: set[str]) -> str:
    while True:
        name = (
            f"{rng.choice(_FIRST_NAMES)} {rng.choice(string.ascii_uppercase)}. "
            f"{rng.choice(_LAST_NAMES)}"
        )
        if name not in used_names:
            used_names.add(name)
            return name


def generate_datasets(
    train_count: int = 1000,
    validation_count: int = 200,
    gold_draft_count: int = 30,
    seed: int = 42,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    for name, count in (
        ("train_count", train_count),
        ("validation_count", validation_count),
        ("gold_draft_count", gold_draft_count),
    ):
        if count < 0:
            raise ValueError(f"{name} cannot be negative")
    rng = random.Random(seed)
    rng = random.Random(seed)
    used_names: set[str] = set()

    train = [
        _make_record("train", index, rng, used_names, include_entities=True)
        for index in range(train_count)
    ]
    validation = [
        _make_record("validation", index, rng, used_names, include_entities=True)
        for index in range(validation_count)
    ]
    gold_drafts = [
        _make_record("gold", index, rng, used_names, include_entities=False)
        for index in range(gold_draft_count)
    ]
    return train, validation, gold_drafts


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic clinical data")
    parser.add_argument("--train-count", type=int, default=1000)
    parser.add_argument("--validation-count", type=int, default=200)
    parser.add_argument("--gold-draft-count", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--synthetic-dir", type=Path, default=SYNTHETIC_DIR)
    parser.add_argument(
        "--gold-drafts-path",
        type=Path,
        default=GOLD_DIR / "test_drafts.jsonl",
    )
    args = parser.parse_args()

    train, validation, gold_drafts = generate_datasets(
        train_count=args.train_count,
        validation_count=args.validation_count,
        gold_draft_count=args.gold_draft_count,
        seed=args.seed,
    )
    _write_jsonl(args.synthetic_dir / "train.jsonl", train)
    _write_jsonl(args.synthetic_dir / "validation.jsonl", validation)
    _write_jsonl(args.gold_drafts_path, gold_drafts)

    print(
        f"Wrote {len(train)} train notes, {len(validation)} validation notes, "
        f"and {len(gold_drafts)} unlabeled gold-test drafts."
    )
    print(f"Gold drafts require manual annotation before evaluation: {args.gold_drafts_path}")


if __name__ == "__main__":
    main()
