import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-3-5-20251001"
MAX_TOKENS = 1024

_api_key = os.getenv("ANTHROPIC_API_KEY")
if not _api_key:
    raise RuntimeError("ANTHROPIC_API_KEY is not set in environment variables")

_client = anthropic.Anthropic(api_key=_api_key)


def complete(system_prompt: str, user_input: str) -> str:
    message = _client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
    )
    return message.content[0].text
