# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- FastAPI application with four endpoints: `/health`, `/summarize`, `/classify-idea`, `/research-agenda`
- Pydantic models with enum enforcement for idea types and context values
- Anthropic Claude Haiku integration via single `complete()` function
- Markdown-based prompt files for summarization, classification, and research agenda generation
- Service layer with JSON parsing and markdown fence stripping
- CORS middleware configured for demo use
- Render deployment config (`render.yaml`)
- Project README with endpoint reference, setup, and deploy instructions
- PRD aligned to implemented scope
- ADR-0001: Use Anthropic as sole LLM provider
