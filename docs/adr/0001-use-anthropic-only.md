# ADR-0001: Use Anthropic as sole LLM provider

**Date:** 2026-04-04
**Status:** Accepted

## Context

The original PRD specified dual LLM provider support — both OpenAI and Anthropic — with a provider abstraction layer controlled by an `LLM_PROVIDER` environment variable. This would have required separate client implementations, a routing layer, and testing across both providers before the April 10 deadline.

The build prompt overrode this decision explicitly: "No provider switching. No abstraction layer. Anthropic only."

## Decision

Use Anthropic Claude Haiku (`claude-haiku-3-5-20251001`) as the sole LLM provider. The LLM client exposes a single `complete(system_prompt, user_input)` function that calls the Anthropic SDK directly. No abstraction layer, no provider configuration.

## Consequences

- Simpler codebase — one client, one SDK, one API key
- Faster to ship within the class deadline
- No need to test prompt behavior across different models
- Adding a second provider later requires introducing an abstraction layer — moved to V2 backlog
- Single vendor dependency for LLM calls
