import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.deidentification.deidentifier import deidentify
from app.deidentification.rehydrator import rehydrate


def main() -> None:
    sample_note = (
        "Patient Alex Morgan, DOB 01/02/1987, was seen on 08/14/2025. "
        "Contact: alex.morgan@example.org or (415) 555-0132. "
        "MRN: SYN-TRAIN-000123."
    )

    masked_text, mapping = deidentify(sample_note)
    restored_text = rehydrate(masked_text, mapping)

    print("Masked text:")
    print(masked_text)
    print("\nPlaceholder mapping:")
    print(json.dumps(mapping, indent=2, sort_keys=True))
    print("\nRestored text:")
    print(restored_text)


if __name__ == "__main__":
    main()
