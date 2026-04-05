# Session Summary — April 4, 2026

## What Was Built

Built and deployed the **Principal Idea Backlog API** — a FastAPI application that transforms rough ideas into structured, actionable output using Anthropic's Claude Haiku.

### Endpoints Delivered

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Returns status and UTC timestamp |
| POST | `/summarize` | Cleans up raw idea text into a backlog-ready summary |
| POST | `/classify-idea` | Classifies idea type, returns confidence and actionable next step |
| POST | `/research-agenda` | Generates 3–5 research questions to unblock scoping |

### Key Decisions

- **Anthropic-only** — PRD originally specified dual-provider support (OpenAI + Anthropic). Simplified to Anthropic-only for V1. Documented in ADR-0001.
- **Model ID fix** — PROMPT specified `claude-haiku-3-5-20251001` which doesn't exist. Updated to `claude-haiku-4-5-20251001`.
- **No provider abstraction** — single `complete()` function calling Anthropic SDK directly.

### Infrastructure

- **GitHub repo:** `afoxnyc3/principal-intake` (public)
- **Deployed URL:** https://principal-intake.onrender.com
- **Swagger UI:** https://principal-intake.onrender.com/docs
- **Render tier:** Free (cold starts ~50 seconds after inactivity)

### Files Created

```
principal-intake/
├── .gitignore
├── CHANGELOG.md
├── PRD.md (updated to match build)
├── PROMPT.md
├── docs/
│   ├── adr/
│   │   ├── README.md
│   │   └── 0001-use-anthropic-only.md
│   ├── prompt-variations.md
│   └── session-summary-2026-04-04.md
└── principal_api/
    ├── .env.example
    ├── README.md
    ├── render.yaml
    ├── requirements.txt
    └── app/
        ├── main.py
        ├── models/
        │   ├── request_models.py
        │   └── response_models.py
        ├── prompts/
        │   ├── __init__.py
        │   ├── summarize.md
        │   ├── classify.md
        │   └── research.md
        ├── routes/
        │   ├── health.py
        │   ├── summarize.py
        │   ├── classify.py
        │   └── research.py
        └── services/
            ├── llm_client.py
            ├── summarizer.py
            ├── classifier.py
            └── researcher.py
```

### Testing Performed

- All 4 endpoints tested locally and against deployed URL
- 5 real Principal ideas run through the full pipeline (summarize → classify → research)
- Pydantic enum enforcement verified — invalid values raise ValidationError
- LLM errors confirmed to return HTTP 502 (not 500)
- Prompt variation experiments completed: 3 variations per endpoint, 9 total tests

### Commits

1. `499a619` — Initial build: Principal Idea Backlog API
2. `20a5f58` — Fix model ID: claude-haiku-3-5 → claude-haiku-4-5
3. `8caecd3` — Add prompt variation experiments for all 3 LLM endpoints

---

## What's Left to Complete the Assignment

### 1. Screenshots of all endpoints working
Take screenshots from Swagger UI showing successful responses for each endpoint. You already have some from today's session — collect them into the submission doc.

### 2. Prompt engineering summary (2–3 paragraphs)
Read https://www.promptingguide.ai/ and write a summary of what you learned about prompt engineering, focusing on techniques that helped improve the prompts in this project. Connect it to the prompt variation experiments in `docs/prompt-variations.md`.

### 3. Submission document (Google Doc or Notion)
Assemble the final submission with:
- Deployed Render URL: https://principal-intake.onrender.com
- GitHub repo link: https://github.com/afoxnyc3/principal-intake
- Screenshots of all endpoints working
- Prompt variations with example outputs and analysis (pull from `docs/prompt-variations.md`)
- Prompt engineering summary paragraphs

### Deadline
**Friday, April 10, 2026**
