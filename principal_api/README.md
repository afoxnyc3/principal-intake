# Principal Idea Backlog API

A lightweight FastAPI service built for Principal — an AI development and consulting company. It transforms rough ideas, talk-to-text notes, and shorthand thoughts into structured, actionable output: clean summaries, idea classifications with next steps, and focused research agendas. Powered by Anthropic's Claude Haiku.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Service health check with UTC timestamp |
| POST | `/summarize` | Clean up raw idea text into a backlog-ready summary |
| POST | `/classify-idea` | Classify idea type and return an actionable next step |
| POST | `/research-agenda` | Generate 3–5 research questions to unblock scoping |

### `GET /health`

**Response**
```json
{
  "status": "ok",
  "timestamp": "2026-04-04T14:00:00+00:00"
}
```

### `POST /summarize`

**Request**
```json
{
  "text": "we should build an intake agent that qualifies leads before they hit the calendar",
  "max_length": 140,
  "context": "client_opportunity"
}
```

**Response**
```json
{
  "summary": "Build a lead qualification agent to screen inbound leads before they reach the booking calendar."
}
```

`context` values: `client_opportunity`, `internal_build`, `research`, `business_development`, `process_improvement`, `general` (default).

### `POST /classify-idea`

**Request**
```json
{
  "text": "we should build an intake agent that qualifies leads before they hit the calendar"
}
```

**Response**
```json
{
  "type": "client_opportunity",
  "confidence": 0.91,
  "next_step": "Add to Principal pipeline and draft a one-pager for prospective clients."
}
```

`type` values: `client_opportunity`, `internal_build`, `research`, `business_development`, `process_improvement`.

### `POST /research-agenda`

**Request**
```json
{
  "text": "thinking about building a lead qualification agent for law firms"
}
```

**Response**
```json
{
  "questions": [
    "What CRMs do mid-size law firms typically use?",
    "Are there existing intake automation tools in the legal tech space?",
    "What compliance considerations apply to client data in legal AI?"
  ],
  "rationale": "These gaps need answers before scoping or proposing this as a client engagement."
}
```

## Local Setup

```bash
cd principal_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
uvicorn app.main:app --reload
```

Swagger UI available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Deploy to Render

1. Push this repo to GitHub
2. Connect the repo in Render
3. Set the root directory to `principal_api`
4. Add `ANTHROPIC_API_KEY` as an environment variable in Render
5. Render will use `render.yaml` for build and start commands

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude Haiku |
