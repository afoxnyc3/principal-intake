from pathlib import Path

_dir = Path(__file__).parent

SUMMARIZE_PROMPT: str = (_dir / "summarize.md").read_text()
CLASSIFY_PROMPT: str = (_dir / "classify.md").read_text()
RESEARCH_PROMPT: str = (_dir / "research.md").read_text()
