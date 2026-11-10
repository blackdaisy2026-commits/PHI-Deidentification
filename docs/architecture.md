# Architecture

Planned flow:

Synthetic clinical note -> transformer detector + structured-identifier recognizers
-> contextual resolution -> span merging -> placeholder mapping -> masked text
-> LLM (masked text only) -> response validation -> rehydration.

The mapping must remain local to the gateway request and must never be sent to an external LLM.
