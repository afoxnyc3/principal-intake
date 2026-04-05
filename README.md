# Principal Intake

A lightweight FastAPI service that turns rough ideas, voice notes, and shorthand thoughts into structured, actionable output. Built for [Principal](https://principal.dev), powered by Claude Haiku.

## What it does

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Service health check |
| `POST /summarize` | Clean raw text into a backlog-ready summary |
| `POST /classify-idea` | Classify idea type + suggest next step |
| `POST /research-agenda` | Generate 3–5 questions to unblock scoping |

## Quick start

```bash
cd principal_api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs).

## Deploy

Push to GitHub, connect to Render, set root to `principal_api`, add `ANTHROPIC_API_KEY`. `render.yaml` handles the rest.

## Docs

- API details: [`principal_api/README.md`](principal_api/README.md)
- Product spec: [`PRD.md`](PRD.md)
- Prompt experiments: [`docs/prompt-variations.md`](docs/prompt-variations.md)
