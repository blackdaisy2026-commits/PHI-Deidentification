import os

MODEL_NAME = os.getenv("PHI_MODEL_NAME", "mkocher/hipaa-phi-detector")
MODEL_OUTPUT_DIR = "models/fine_tuned"
MAX_LENGTH = 512

PHI_CATEGORIES = [
    "NAME", "LOCATION", "DATE", "AGE", "PHONE", "FAX", "EMAIL",
    "SSN", "MRN", "HEALTH_PLAN", "ACCOUNT", "LICENSE", "URL", "IP",
]
