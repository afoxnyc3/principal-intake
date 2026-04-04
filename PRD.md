# PRD — Principal Idea Backlog API

## 1. Project Overview

**Project Name:** Principal Idea Backlog API
**Project Type:** FastAPI + LLM API
**Company:** Principal — AI development and consulting
**Primary Goal:** Transform rough ideas, talk-to-text notes, and shorthand thoughts into structured, actionable output — built for the operational workflow of a lean AI company.

This project satisfies the class assignment requirements while serving as a real internal tool for Principal:

- `GET /health`
- `POST /summarize`
- `POST /classify-idea`
- `POST /research-agenda`

---

## 2. Problem Statement

Principal operates at the intersection of building and advising. Ideas surface constantly — in client conversations, between meetings, during builds, and during strategic thinking. They arrive as:

- talk-to-text notes
- shorthand reminders
- rough client observations
- internal tooling concepts
- business development thoughts

Without a lightweight triage system, these ideas are:

- hard to route to the right place
- easy to lose or forget
- too rough to act on immediately
- mixed together with no signal about what to do next

Principal needs a simple service that captures a raw idea and returns clean, structured output that tells you what the idea is, where it belongs, and what to do next.

---

## 3. Project Objective

Build a small FastAPI application that:

1. confirms service health
2. summarizes raw idea text into a concise, actionable summary
3. classifies the idea type and recommends an immediate next step
4. generates a focused research agenda to unblock scoping or decision-making

The app should be simple, fast, and deployable within one week.

---

## 4. Why This Project

### Class alignment

The assignment requires:

- a health endpoint
- a summarization endpoint
- a third LLM-powered endpoint

This project satisfies all three requirements and extends naturally to a fourth.

### Real-world value for Principal

This API serves as a lightweight idea triage pipeline:

> Raw thought → clean summary → idea classification → research agenda

Every output maps directly to a real workflow action: adding to a roadmap, drafting a proposal, opening a Notion note, or scheduling a research block.

---

## 5. Target User

### Primary user

Alex Fox, Principal — capturing ideas across client work, internal builds, and business development.

### Typical workflow

- user dictates or types a rough idea
- `/summarize` returns a clean, backlog-ready version
- `/classify-idea` returns the idea type and recommended next step
- `/research-agenda` returns focused questions to answer before scoping
- user routes the output to the right system (roadmap, proposal, Notion, calendar)

---

## 6. Scope

### In Scope

- FastAPI backend
- 4 endpoints
- JSON request and response bodies
- Anthropic Claude Haiku as sole LLM provider
- Markdown-based prompt files loaded as Python string constants
- Pydantic enum enforcement on classified output
- Deployment to Render
- Swagger docs via FastAPI

### Out of Scope (V1)

- Dual LLM provider support (V2 consideration)
- Spec generation (V2 — see Section 14)
- Jira / Notion integration
- Authentication
- Persistent database
- Task generation
- Backlog storage
- Mobile frontend / PWA
- Agent orchestration

---

## 7. Functional Requirements

### 7.1 `GET /health`

#### Purpose

Confirms the API is online and responsive.

#### Response

```json
{
  "status": "ok",
  "timestamp": "2026-04-04T14:00:00+00:00"
}
```

#### Requirements

- returns HTTP 200
- returns status
- returns UTC timestamp

---

### 7.2 `POST /summarize`

#### Purpose

Takes a rough idea and returns a concise, backlog-ready summary. An optional `context` field allows the caller to indicate the nature of the input, enabling the prompt to tune its framing accordingly.

#### Request

```json
{
  "text": "we should build an intake agent that qualifies leads before they hit the calendar",
  "max_length": 140,
  "context": "client_opportunity"
}
```

#### `context` field values

| Value | Description |
|---|---|
| `client_opportunity` | Could become a proposal or engagement |
| `internal_build` | Tool or agent for Principal's own operations |
| `research` | Something to explore before deciding |
| `business_development` | Positioning, partnerships, outreach |
| `process_improvement` | How Principal operates day-to-day |
| `general` | Uncategorized — no framing applied |

`context` is optional. If omitted, defaults to `general`.

#### Response

```json
{
  "summary": "Build a lead qualification agent to screen inbound leads before they reach the booking calendar."
}
```

#### Requirements

- accept free-form text
- accept optional `context` field
- preserve original intent
- do not hallucinate new facts
- return a concise summary
- respect the `max_length` limit

---

### 7.3 `POST /classify-idea`

#### Purpose

Classifies the idea type and returns a recommended next step to route the idea to the right place immediately.

#### Request

```json
{
  "text": "we should build an intake agent that qualifies leads before they hit the calendar"
}
```

#### Response

```json
{
  "type": "client_opportunity",
  "confidence": 0.91,
  "next_step": "Add to Principal pipeline and draft a one-pager for prospective clients."
}
```

#### `type` enum

| Value | Meaning |
|---|---|
| `client_opportunity` | Could become a proposal or engagement |
| `internal_build` | Tool or agent for Principal's own operations |
| `research` | Something to explore before deciding |
| `business_development` | Positioning, partnerships, outreach |
| `process_improvement` | How Principal operates day-to-day |

#### Requirements

- classify idea into one of the five types above
- Pydantic must enforce the type enum — invalid LLM values must raise a validation error
- return confidence between `0.0` and `1.0`
- return a brief, actionable `next_step` grounded in the idea type

---

### 7.4 `POST /research-agenda`

#### Purpose

Given a rough idea, generates a focused set of research questions to answer before scoping, proposing, or building. Returns a research agenda, not research results.

#### Request

```json
{
  "text": "thinking about building a lead qualification agent for law firms"
}
```

#### Response

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

#### Requirements

- return 3–5 focused research questions
- questions must be grounded in the input — no hallucinated assumptions
- return a brief rationale explaining why these questions matter
- do not return research answers — agenda only

---

## 8. Non-Functional Requirements

- API must be stateless
- API must return JSON
- Input validation must use Pydantic
- API key must be loaded from environment variables
- Typical responses should feel fast enough for interactive use
- Codebase should be simple and readable

---

## 9. Technical Design

### Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **Anthropic SDK** (Claude Haiku)
- **Uvicorn**
- **Render**

### LLM Provider

Anthropic Claude Haiku (`claude-haiku-3-5-20251001`) is the sole LLM provider. The LLM client exposes a single `complete(system_prompt, user_input)` function with no provider abstraction layer.

```env
ANTHROPIC_API_KEY=sk-ant-...
```

### Folder Structure

```text
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

### LLM Client

`llm_client.py` exposes a single `complete(system_prompt: str, user_input: str) -> str` function. It uses the Anthropic SDK directly — no abstraction layer, no provider switching. Routes and services call only `complete()`.

### Prompt Loading

`prompts/__init__.py` reads each `.md` file at startup and exposes them as named string constants:

```python
SUMMARIZE_PROMPT: str   # loaded from summarize.md
CLASSIFY_PROMPT: str    # loaded from classify.md
RESEARCH_PROMPT: str    # loaded from research.md
```

---

## 10. Prompt Design Principles

### Summarize prompt (`summarize.md`)

- preserve meaning
- improve clarity
- stay concise — one clean sentence
- avoid adding information not in the source
- use the `context` value to tune framing when provided

### Classify prompt (`classify.md`)

- classify into exactly one of the five idea types
- return valid JSON only — no preamble
- `next_step` must be specific and actionable, not generic
- interpret Principal's operational language correctly

### Research prompt (`research.md`)

- return 3–5 questions only — not answers
- questions must be grounded in the input
- rationale must explain why these questions unblock progress
- return valid JSON only — no preamble

---

## 11. Example Use Cases

### Example 1 — Client opportunity

**Input**
> we should build an intake agent that qualifies leads before they hit the calendar

**Summarize** → `Build a lead qualification agent to screen inbound leads before they reach the booking calendar.`

**Classify** → `client_opportunity` / `"Add to Principal pipeline and draft a one-pager for prospective clients."`

**Research agenda** →
- What intake workflows do service businesses typically use today?
- Are there existing qualification agent frameworks to build on?
- What's the right handoff point between agent and human in a sales flow?

---

### Example 2 — Internal build

**Input**
> I want an agent that monitors my email and flags anything that needs a response today

**Summarize** → `Build an internal email monitoring agent that identifies and flags time-sensitive messages requiring same-day response.`

**Classify** → `internal_build` / `"Add to Principal internal roadmap and define acceptance criteria."`

**Research agenda** →
- What email APIs support real-time monitoring without polling overhead?
- How should urgency be defined — sender, keywords, thread age?
- What notification surface makes most sense — Slack, Teams, or SMS?

---

### Example 3 — Business development

**Input**
> I should post more about what we're building, the agent architecture stuff is resonating on LinkedIn

**Summarize** → `Increase LinkedIn content cadence around Principal's agent architecture work to capitalize on audience engagement.`

**Classify** → `business_development` / `"Draft a content calendar and identify 3 post topics from recent builds."`

**Research agenda** →
- What agent architecture topics are currently getting traction on LinkedIn?
- What posting cadence drives consistent growth without audience fatigue?
- Which Principal builds are most transferable to public case studies?

---

## 12. Success Criteria

The project is successful if:

- all four endpoints work
- the app is deployed successfully on Render
- the summarization output is clean and usable
- the `context` field demonstrably affects summary framing
- the classification type enum is enforced by Pydantic
- the `next_step` field is specific and actionable
- the research agenda returns grounded, useful questions
- the project can be demonstrated with realistic Principal examples
- the project clearly aligns with the assignment requirements

---

## 13. Risks

### Risk 1: Over-scoping

V2 features (spec generation, dual providers, integrations, frontend) are explicitly excluded. Ship V1 first.

### Risk 2: Hallucinated summaries

Prompt design and tight output constraints reduce this. Prompts explicitly instruct the model not to add information not present in the input.

### Risk 3: Weak classify confidence

The LLM may struggle with ambiguous ideas that span multiple types. The prompt instructs it to pick the single strongest match and explain why in the `next_step`.

---

## 14. V2 Backlog

### Dual LLM Provider Support

Add OpenAI as an alternative provider, controlled by an `LLM_PROVIDER` environment variable with an abstraction layer that routes to the active provider.

### `POST /generate-spec`

Takes a classified, summarized idea and generates a structured spec — the natural end of the triage pipeline.

```json
{
  "title": "Lead Qualification Agent — Legal Vertical",
  "problem": "...",
  "proposed_solution": "...",
  "open_questions": [...],
  "suggested_next_steps": [...]
}
```

This completes the full pipeline:

> Raw idea → summarize → classify → research agenda → **spec**

---

## 15. Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude Haiku |

---

## 16. Final Positioning Statement

**Principal Idea Backlog API** is a lightweight FastAPI service built for Principal — an AI development and consulting company. It transforms rough ideas into clean summaries, classifies them into actionable types, and generates focused research agendas to unblock scoping and decision-making. Powered by Anthropic's Claude Haiku, it uses markdown-based prompt files for clean iteration and is designed to serve as the foundation for a future full-featured idea triage and spec generation pipeline.
