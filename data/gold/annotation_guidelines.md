# Gold Test Annotation Guidelines

- Use synthetic notes only; never use real patient data.
- Hand-label at least 20 notes (30 is a useful initial target).
- Record exact character offsets using half-open spans: `start` inclusive, `end` exclusive.
- Label all required PHI categories consistently.
- Preserve years where required, but mask other calendar-date components.
- Mask ages over 89; do not mask younger ages solely because they are ages.
- Preserve relative clinical durations such as `3 days post-op`.
- Record ambiguous cases and adjudication decisions.
- Keep test notes separate from training and validation templates/identities.

## JSONL format

Each line is one JSON object. Training and validation records use:

```json
{"id":"train-000001","text":"...","entities":[{"start":0,"end":5,"text":"...","label":"NAME"}]}
```

Offsets are Python string character offsets, with `start` inclusive and `end`
exclusive. The `text` field on an entity must exactly match that slice of the
note. Allowed labels in the initial synthetic generator are `NAME`, `AGE`,
`DATE`, `PHONE`, `EMAIL`, `MRN`, and `LOCATION`.

Generated gold-test drafts intentionally contain only `id` and `text`. Copy
their notes into `data/gold/test.jsonl` and add a manually reviewed `entities`
array before evaluation. Do not use the generated annotations as gold labels.
