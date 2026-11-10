from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.deidentification.deidentifier import deidentify
from app.deidentification.rehydrator import rehydrate

app = FastAPI(title="PHI De-identification Gateway", version="0.1.0")


class TextRequest(BaseModel):
    text: str = Field(default="", description="Clinical text to de-identify")


class RehydrateRequest(BaseModel):
    text: str = Field(default="", description="Masked text to restore")
    mapping: dict[str, str] = Field(default_factory=dict, description="Placeholder map")


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "stage": "rule-based-demo"}


@app.post("/deidentify")
def deidentify_endpoint(payload: TextRequest) -> dict[str, Any]:
    masked_text, mapping = deidentify(payload.text)
    return {"masked_text": masked_text, "mapping": mapping}


@app.post("/rehydrate")
def rehydrate_endpoint(payload: RehydrateRequest) -> dict[str, Any]:
    return {"rehydrated_text": rehydrate(payload.text, payload.mapping)}
