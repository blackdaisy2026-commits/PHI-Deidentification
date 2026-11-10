import json
import re
import sys

import pytest

from scripts.generate_dataset import _write_jsonl, generate_datasets, main


def test_generated_datasets_are_reproducible_and_span_offsets_are_exact():
    first = generate_datasets(train_count=8, validation_count=3, gold_draft_count=2, seed=7)
    second = generate_datasets(train_count=8, validation_count=3, gold_draft_count=2, seed=7)

    assert first == second
    train, validation, _ = first
    for record in train + validation:
        for entity in record["entities"]:
            assert record["text"][entity["start"]:entity["end"]] == entity["text"]
            if entity["label"] == "DATE":
                assert len(entity["text"]) == 5
                assert re.match(
                    r"/\d{4}", record["text"][entity["end"]:entity["end"] + 5]
                )
            if entity["label"] == "AGE":
                assert int(entity["text"]) > 89
        assert "@example.test" in record["text"]


def test_gold_test_drafts_have_no_machine_generated_labels():
    train, validation, gold_drafts = generate_datasets(
        train_count=4,
        validation_count=2,
        gold_draft_count=3,
        seed=11,
    )

    assert all("entities" in record for record in train + validation)
    assert all(set(record) == {"id", "text"} for record in gold_drafts)
    assert all("@example.test" in record["text"] for record in gold_drafts)
    assert all("patient.train." in record["text"] for record in train)
    assert all("patient.validation." in record["text"] for record in validation)
    assert all("patient.gold." in record["text"] for record in gold_drafts)

    def labeled_names(records):
        return {
            entity["text"]
            for record in records
            for entity in record["entities"]
            if entity["label"] == "NAME"
        }

    train_names = labeled_names(train)
    validation_names = labeled_names(validation)
    gold_names = {
        record["text"].split(", age", maxsplit=1)[0].split(": ", maxsplit=1)[-1]
        .removeprefix("Patient ")
        for record in gold_drafts
    }
    assert train_names.isdisjoint(validation_names)
    assert train_names.isdisjoint(gold_names)
    assert validation_names.isdisjoint(gold_names)


def test_write_jsonl_creates_parent_directories_and_round_trips(tmp_path):
    output = tmp_path / "nested" / "notes.jsonl"
    records = [{"id": "train-000001", "text": "synthetic note", "entities": []}]

    _write_jsonl(output, records)

    assert [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()] == records


def test_negative_record_counts_are_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        generate_datasets(train_count=-1)


def test_command_line_entry_point_writes_separate_splits(tmp_path, monkeypatch):
    synthetic_dir = tmp_path / "synthetic"
    gold_drafts_path = tmp_path / "gold" / "test_drafts.jsonl"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "generate_dataset.py",
            "--train-count",
            "2",
            "--validation-count",
            "1",
            "--gold-draft-count",
            "1",
            "--synthetic-dir",
            str(synthetic_dir),
            "--gold-drafts-path",
            str(gold_drafts_path),
        ],
    )

    main()

    assert len((synthetic_dir / "train.jsonl").read_text(encoding="utf-8").splitlines()) == 2
    assert len((synthetic_dir / "validation.jsonl").read_text(encoding="utf-8").splitlines()) == 1
    assert len(gold_drafts_path.read_text(encoding="utf-8").splitlines()) == 1
