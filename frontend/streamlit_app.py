import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.deidentification.deidentifier import deidentify
from app.deidentification.rehydrator import rehydrate


st.set_page_config(page_title="PHI De-identification Gateway", page_icon="🛡️")

st.title("PHI De-identification Gateway")
st.warning("Synthetic demonstration only. Do not enter real patient information.")

sample_note = (
    "Patient Alex Morgan, DOB 01/02/1987, was seen on 08/14/2025. "
    "Contact: alex.morgan@example.org or (415) 555-0132. "
    "MRN: SYN-TRAIN-000123."
)

text = st.text_area("Clinical note", value=sample_note, height=220)

if st.button("De-identify note"):
    masked_text, mapping = deidentify(text)
    rehydrated_text = rehydrate(masked_text, mapping)

    st.subheader("Masked text")
    st.code(masked_text)

    st.subheader("Placeholder mapping")
    st.json(mapping)

    st.subheader("Round-trip check")
    st.success(rehydrated_text == text)
    st.code(rehydrated_text)
