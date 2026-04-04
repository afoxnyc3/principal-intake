import json
import re

from app.prompts import CLASSIFY_PROMPT
from app.services.llm_client import complete


def _strip_fences(text: str) -> str:
    return re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()


def classify(text: str) -> dict:
    raw = complete(CLASSIFY_PROMPT, text)
    return json.loads(_strip_fences(raw))
