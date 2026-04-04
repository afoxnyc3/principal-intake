# Claude Code — Principal Idea Backlog API

## Mission

Scaffold and implement the Principal Idea Backlog API — a FastAPI application that transforms rough ideas into structured, actionable output. This is a class assignment with a real-world use case. Build it clean, keep it simple, and make it deployable.

**Deadline:** April 10, 2026
**Deploy target:** Render
**LLM provider:** Anthropic (`claude-haiku-3-5`)

---

## Reference Document

The full PRD is in `PRD.md` at the project root. Read it completely before writing any code. All design decisions are finalized — do not improvise or extend scope.

---

## What to Build

Four endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Returns status and UTC timestamp |
| POST | `/summarize` | Cleans up raw idea text into a backlog-ready summary |
| POST | `/classify-idea` | Classifies idea type and returns an actionable next step |
| POST | `/research-agenda` | Generates 3–5 research questions to unblock scoping |

---

## Implementation Order

Build in this exact sequence. Do not skip ahead.

### Step 1 — Project scaffold

Create the full folder structure:

```
principal_api/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── summarize.py
│   │   ├── classify.py
│   │   └── research.py
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/
│   │   ├── llm_client.py
│   │   ├── summarizer.py
│   │   ├── classifier.py
│   │   └── researcher.py
│   └── prompts/
│       ├── __init__.py
│       ├── summarize.md
│       ├── classify.md
│       └── research.md
├── requirements.txt
├── .env.example
├── render.yaml
└── README.md
```

Initialize `main.py` with a FastAPI app instance, register all four routers, and configure CORS to allow all origins for demo purposes.

---

### Step 2 — Pydantic models

**`request_models.py`**

- `SummarizeRequest`: `text: str`, `max_length: int = 140`, `context: ContextEnum = "general"`
- `ClassifyRequest`: `text: str`
- `ResearchRequest`: `text: str`

`ContextEnum` values: `client_opportunity`, `internal_build`, `research`, `business_development`, `process_improvement`, `general`

**`response_models.py`**

- `HealthResponse`: `status: str`, `timestamp: datetime`
- `SummarizeResponse`: `summary: str`
- `ClassifyResponse`: `type: IdeaTypeEnum`, `confidence: float`, `next_step: str`
- `ResearchResponse`: `questions: list[str]`, `rationale: str`

`IdeaTypeEnum` values: `client_opportunity`, `internal_build`, `research`, `business_development`, `process_improvement`

Pydantic must enforce all enums. An invalid value from the LLM must raise a validation error — it must never pass silently.

---

### Step 3 — Prompt files

Write all three prompts as markdown files. Each prompt must:

- instruct the model to return **JSON only** — no preamble, no explanation, no markdown fences
- be explicit about the exact output schema
- be grounded in the input — never hallucinate facts not present in the source

**`summarize.md`**

You are a concise technical writer. Your job is to take a rough idea, note, or thought and rewrite it as a single clean sentence suitable for a product backlog.

Rules:
- Preserve the original intent exactly
- Do not add facts, features, or assumptions not present in the input
- Respect the max_length character limit if provided
- If a context type is provided, use it to frame the language appropriately:
  - client_opportunity: frame as a potential service or product offering
  - internal_build: frame as an internal tool or capability
  - research: frame as an area to investigate
  - business_development: frame as a strategic or outreach initiative
  - process_improvement: frame as an operational change
  - general: no specific framing

Return JSON only:
```json
{"summary": "..."}
```

**`classify.md`**

You are an idea classification engine for Principal, an AI development and consulting company.

Classify the input into exactly one of these types:
- client_opportunity: Could become a client proposal or engagement
- internal_build: A tool or agent to build for Principal's own operations
- research: Something to explore or investigate before deciding
- business_development: Positioning, partnerships, content, or outreach
- process_improvement: How Principal operates day to day

Rules:
- Pick the single strongest match — do not hedge or split
- The next_step must be specific and immediately actionable — not generic advice
- Confidence must be between 0.0 and 1.0
- Return JSON only — no preamble, no explanation outside the JSON object

Return JSON only:
```json
{"type": "...", "confidence": 0.0, "next_step": "..."}
```

**`research.md`**

You are a research strategist for Principal, an AI development and consulting company.

Given a rough idea, generate a focused research agenda — the specific questions that need answers before this idea can be scoped, proposed, or built.

Rules:
- Return exactly 3 to 5 questions
- Questions must be grounded in the input — do not invent assumptions
- Questions should unblock real decisions, not restate the obvious
- The rationale must explain in one sentence why these questions matter
- Return JSON only — no preamble, no explanation outside the JSON object

Return JSON only:
```json
{"questions": ["...", "...", "..."], "rationale": "..."}
```

**`prompts/__init__.py`**

Load all three files as string constants at startup:

```python
from pathlib import Path

_dir = Path(__file__).parent

SUMMARIZE_PROMPT: str = (_dir / "summarize.md").read_text()
CLASSIFY_PROMPT: str = (_dir / "classify.md").read_text()
RESEARCH_PROMPT: str = (_dir / "research.md").read_text()
```

---

### Step 4 — LLM client

**`llm_client.py`**

Single function: `complete(system_prompt: str, user_input: str) -> str`

- Uses the Anthropic SDK
- Model: `claude-haiku-3-5-20251001`
- `max_tokens`: 1024
- Loads `ANTHROPIC_API_KEY` from environment via `python-dotenv`
- Raises a descriptive exception if the key is missing
- Returns the text content of the first message block

No provider switching. No abstraction layer. Anthropic only.

---

### Step 5 — Service layer

Each service calls `llm_client.complete()` and parses the JSON response.

**`summarizer.py`**

```python
def summarize(text: str, max_length: int, context: str) -> str
```

Builds the user input string from the arguments, calls `complete()` with `SUMMARIZE_PROMPT`, parses the JSON, returns `summary`.

**`classifier.py`**

```python
def classify(text: str) -> dict
```

Calls `complete()` with `CLASSIFY_PROMPT`, parses JSON, returns the dict. Pydantic validation happens in the route layer.

**`researcher.py`**

```python
def research(text: str) -> dict
```

Calls `complete()` with `RESEARCH_PROMPT`, parses JSON, returns the dict. Pydantic validation happens in the route layer.

All three services must strip markdown fences from the LLM response before parsing JSON, in case the model wraps output in backticks despite the prompt instructions.

---

### Step 6 — Routes

**`health.py`**

```python
@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
```

**`summarize.py`**

Accepts `SummarizeRequest`, calls `summarizer.summarize()`, returns `SummarizeResponse`.

**`classify.py`**

Accepts `ClassifyRequest`, calls `classifier.classify()`, validates result into `ClassifyResponse` using Pydantic, returns response.

**`research.py`**

Accepts `ResearchRequest`, calls `researcher.research()`, validates result into `ResearchResponse` using Pydantic, returns response.

All routes must return proper HTTP error responses for LLM failures — 502 with a descriptive message, not a raw 500.

---

### Step 7 — Deploy config and supporting files

**`requirements.txt`**

```
fastapi
uvicorn[standard]
anthropic
pydantic
python-dotenv
```

**`.env.example`**

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**`render.yaml`**

```yaml
services:
  - type: web
    name: principal-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
```

**`README.md`**

Include:
- Project description (one paragraph)
- Endpoint reference table with example request/response for each endpoint
- Local setup instructions
- Render deploy instructions
- Environment variable reference

---

## Code Standards

- Functions: 25 lines max
- Files: 150 lines max
- No inline comments explaining what the code does — write code that speaks for itself
- All environment variables loaded via `python-dotenv` at startup
- No hardcoded strings for model names or API endpoints — use constants
- Pydantic models for all request and response bodies — no raw dicts in route handlers

---

## Definition of Done

- [ ] All four endpoints return correct responses locally
- [ ] `/health` returns UTC timestamp
- [ ] `/summarize` respects `max_length` and `context`
- [ ] `/classify-idea` returns a valid `IdeaTypeEnum` value enforced by Pydantic
- [ ] `/research-agenda` returns 3–5 questions and a rationale
- [ ] LLM errors return HTTP 502, not 500
- [ ] App runs with `uvicorn app.main:app --reload`
- [ ] Swagger UI loads at `/docs` with all endpoints documented
- [ ] `render.yaml` is present and correct
- [ ] `.env.example` is present
- [ ] `README.md` is complete
- [ ] App deploys successfully on Render
- [ ] All endpoints tested against deployed URL
