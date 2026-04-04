import json
import re

from app.prompts import RESEARCH_PROMPT
from app.services.llm_client import complete


def _strip_fences(text: str) -> str:
    return re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()


def research(text: str) -> dict:
    raw = complete(RESEARCH_PROMPT, text)
    return json.loads(_strip_fences(raw))
