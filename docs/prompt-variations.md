# Prompt Variation Experiments

**Test idea used across all variations:**
> "I want to build a chatbot that helps small business owners file their quarterly taxes"

---

## `/summarize` — 3 Prompt Variations

### Variation 1: Detailed role + rules (SELECTED)

**Prompt approach:** Assigns a specific role ("concise technical writer"), provides explicit rules for each context type, and constrains output format.

**Output:**
```json
{"summary": "Offer a chatbot service that guides small business owners through quarterly tax filing."}
```

### Variation 2: Minimal instruction

**Prompt approach:** Bare minimum — just tells the model to rewrite and return JSON. No role, no rules, no context handling.

**Output:**
```json
{"summary": "Build a chatbot that guides small business owners through quarterly tax filing."}
```

### Variation 3: Product manager role + verb-first constraint

**Prompt approach:** Assigns a "product manager" role, adds a structural constraint (start with a verb), and uses numbered requirements instead of bullet rules.

**Output:**
```json
{"summary": "Build a chatbot service that guides small business owners through quarterly tax filing."}
```

### Analysis — Which worked best?

**Variation 1 (detailed role + rules) performed best.** The key difference is context-awareness. When given `context: client_opportunity`, V1 produced "Offer a chatbot service" — framing it as something Principal could sell. V2 and V3 both defaulted to "Build a chatbot," ignoring the context entirely because their prompts didn't explain context framing.

V2 proves that minimal prompts can produce grammatically correct output, but they miss nuance. V3's verb-first constraint was a good structural idea, but without context-type definitions, the model couldn't apply business framing.

**Key takeaway:** For tasks that require domain-specific framing (not just rewriting), the prompt must explicitly define what each frame means. The model won't infer business context on its own.

---

## `/classify-idea` — 3 Prompt Variations

### Variation 1: Structured rules with company context (SELECTED)

**Prompt approach:** Names the company (Principal), defines each category with a plain-English description, and provides explicit rules about hedging, confidence, and actionability.

**Output:**
```json
{
  "type": "client_opportunity",
  "confidence": 0.85,
  "next_step": "Schedule a discovery call with the requester to understand: (1) their technical vision and constraints, (2) target market size and willingness to pay, (3) whether they want Principal to build it as a service or a one-time engagement, and (4) their timeline and budget."
}
```

### Variation 2: Minimal instruction

**Prompt approach:** One-line instruction with category names only. No company context, no rules about actionability.

**Output:**
```json
{
  "type": "client_opportunity",
  "confidence": 0.85,
  "next_step": "Interview 10-15 small business owners about their current tax filing process, pain points, and willingness to pay for an automated solution to validate market demand and refine the chatbot's core features."
}
```

### Variation 3: Chain-of-thought with intake system framing

**Prompt approach:** Frames the model as an "intake system," uses numbered dimensions instead of bullet rules, and adds "think step by step" instruction.

**Output:**
```json
{
  "type": "client_opportunity",
  "confidence": 0.75,
  "next_step": "Schedule a 30-minute call with the founder to understand: (1) their current business model, (2) whether they're pitching this as a service Principal would build for a client or as a product Principal would build and sell, (3) target market size and willingness to pay, and (4) whether there are existing competitors and their positioning."
}
```

### Analysis — Which worked best?

**Variation 1 (structured rules) performed best overall.** All three correctly classified the idea as `client_opportunity`, but the differences are in confidence calibration and next-step quality.

V1 produced a confident (0.85), specific next step grounded in Principal's actual workflow. V2 was surprisingly good for a minimal prompt — its next step (interviewing small business owners) was concrete and actionable, though it lacks Principal-specific context. V3's chain-of-thought instruction actually lowered confidence to 0.75, which isn't wrong (more deliberation = more uncertainty), but the next step was less decisive — it still needs a call to figure out what the idea even is.

**Key takeaway:** Adding "think step by step" doesn't always improve output. For classification tasks that need a decisive answer, direct rules outperform deliberation prompts. Chain-of-thought is better suited for reasoning-heavy tasks, not triage.

---

## `/research-agenda` — 3 Prompt Variations

### Variation 1: Research strategist role (SELECTED)

**Prompt approach:** Assigns "research strategist" role, emphasizes grounding in input, and requires questions that "unblock real decisions."

**Output:**
```json
{
  "questions": [
    "What specific tax filing scenarios (S-corp, LLC, sole proprietor, etc.) should the chatbot handle first?",
    "What is the regulatory risk or liability exposure if the chatbot provides guidance that differs from official IRS guidance?",
    "Should the chatbot integrate with existing accounting software (QuickBooks, Xero) or operate as a standalone assistant?",
    "What are the key pain points small business owners currently face with quarterly tax filing that a chatbot could uniquely solve?"
  ],
  "rationale": "These questions determine the product scope, legal feasibility, technical architecture, and market fit before committing to development."
}
```

### Variation 2: Minimal instruction

**Prompt approach:** Simple instruction — generate questions, include rationale. No role, no constraints on question quality.

**Output:**
```json
{
  "questions": [
    "What specific tax filing challenges do small business owners currently face, and would they trust an AI chatbot over a human accountant?",
    "How would the chatbot handle variations in tax requirements across different states, business structures, and industries?",
    "What liability and compliance risks exist if the chatbot provides incorrect tax guidance?",
    "Are small business owners willing to pay a subscription fee, and how does pricing compare to existing tax software or accountants?",
    "How would you ensure the chatbot stays current with frequent tax law changes?"
  ],
  "rationale": "These questions identify critical unknowns around user demand, technical scope complexity, legal/liability exposure, market fit, and long-term operational feasibility."
}
```

### Variation 3: Senior strategist with dimensional targeting

**Prompt approach:** "Senior strategist" role with explicit instruction to target different dimensions (market viability, technical feasibility, competitive landscape, regulatory, user behavior). Adds "make the build/no-build decision obvious."

**Output:**
```json
{
  "questions": [
    "What specific tax filing tasks would your chatbot actually handle vs. delegate to accountants, and does this scope remain legally compliant across all 50 states?",
    "How would you acquire small business owners given that CPAs and tax software incumbents (QuickBooks, TurboTax) already have massive distribution and trust?",
    "What liability exposure exists if the chatbot's guidance leads to underpayment, missed deadlines, or audit triggers?",
    "Would small business owners actually trust a chatbot over their existing accountant for something as mission-critical as quarterly tax filing?"
  ],
  "rationale": "Together, these questions expose whether you're solving a real problem with viable product-market fit, or building a nice-to-have in a space where incumbents own distribution and compliance complexity makes scaling legally risky."
}
```

### Analysis — Which worked best?

**Variation 3 (senior strategist with dimensions) produced the highest-quality questions**, but **Variation 1 was selected for production** as the best balance of quality and reliability.

V3's questions are sharper and more confrontational — "Would small business owners actually trust a chatbot?" and "How would you acquire customers given incumbents already own distribution?" These are the real blockers. The dimensional targeting constraint (market, technical, regulatory, competitive, user) forced the model to cover different angles rather than clustering around one concern.

V2 (minimal) produced 5 decent questions, but they're softer — more "what are the challenges?" instead of "would this actually work?" The rationale is also more generic.

V1 sits in the middle — grounded, practical questions with a clean rationale. It was selected for production because it reliably produces useful output without the occasional over-aggressiveness of V3 (which could feel adversarial to a user submitting an idea they're excited about).

**Key takeaway:** Dimensional constraints (requiring each question to target a different concern area) significantly improve question diversity. The "build/no-build decision" framing in V3 made the model more decisive. For production, V1's balanced tone is safer; for internal strategic use, V3 would be the stronger choice.

---

## Summary of Findings

| Technique | Effect | Best for |
|-----------|--------|----------|
| Role assignment ("You are a...") | Gives the model a perspective and tone | All endpoints — consistent improvement |
| Explicit output schema | Prevents extra text, ensures parseable JSON | Required for any structured output |
| Context/framing definitions | Model can't infer business meaning from enum names alone | Domain-specific tasks like summarization |
| "Think step by step" | Increases deliberation, can lower confidence | Complex reasoning — not ideal for triage |
| Dimensional constraints | Forces coverage across different concerns | Research/analysis tasks |
| Minimal prompts | Work for simple tasks, fail on nuanced ones | Quick prototyping only |
