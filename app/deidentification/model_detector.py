def load_detector(model_name: str):
    raise NotImplementedError("Inspect checkpoint labels and implement model loading.")


def detect_model_entities(text: str):
    raise NotImplementedError("Return PHI spans with character offsets and confidence.")
