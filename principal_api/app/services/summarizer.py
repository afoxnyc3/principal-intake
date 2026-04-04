import json
import re

from app.prompts import SUMMARIZE_PROMPT
from app.services.llm_client import complete


def _strip_fences(text: str) -> str:
    return re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()


def summarize(text: str, max_length: int, context: str) -> str:
    user_input = (
        f"Idea: {text}\n"
        f"Max length: {max_length} characters\n"
        f"Context: {context}"
    )
    raw = complete(SUMMARIZE_PROMPT, user_input)
    parsed = json.loads(_strip_fences(raw))
    return parsed["summary"]
