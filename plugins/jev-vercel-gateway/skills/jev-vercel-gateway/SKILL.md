---
name: jev-vercel-gateway
description: Use TypeSafe AI's Jev through Vercel AI Gateway for fast typed Boolean, Choice, and Score decisions, or add Jev evaluation to applications, systems, and scripts. Apply when the user mentions Jev, System One models, ai-cli evaluation, probabilistic classification, routing, scoring, guardrails, or decision layers. Do not use Jev for open-ended prose or code generation.
---

# Jev via Vercel AI Gateway

Use Jev as a typed probabilistic decision function: one shared text or JSON state
in, named Boolean, Choice, and Score answers out. Jev's model ID is
`typesafe-ai/jev`.

## Boundaries

- Jev is a remote, metered service. Send private, proprietary, or regulated
  material only when the user has explicitly asked to use Jev on that material.
  Remove credentials and unrelated sensitive fields first.
- Type-constrained output prevents undeclared answer shapes; it does not make a
  judgment infallible. Calibrate questions and thresholds on representative data.
- Use a generative model, not Jev, when the task needs prose, explanations, code,
  novel labels, or an answer outside a predefined set.
- Keep business side effects outside the model call. Code applies thresholds,
  fallback behavior, review queues, and mutations after inspecting the result.

## Prerequisites

Before the first call in a task, check without printing secrets:

```bash
command -v ai
ai --version
if [[ -n ${AI_GATEWAY_API_KEY:-} ]]; then print -- present; else print -- absent; fi
```

The supported local baseline is Node.js 22+ and `ai-cli` 0.5.1+. If the CLI is
missing, tell the user and install it only when setup or installation is in scope:

```bash
npm install -g ai-cli@latest
```

If `AI_GATEWAY_API_KEY` is absent, stop before a live request and say so. Never
print, log, copy into a command argument, or save the key in a skill or project.

## Choose the mode

- For an immediate decision or a shell pipeline, use `ai evaluate`.
- For a reusable application, service, or library integration, read
  [Application integration](references/application-integration.md).

## Evaluate from the terminal

Pass the complete state on stdin. Output is always JSON.

```bash
printf '%s\n' 'The deployment removes the production database.' |
  ai evaluate --boolean "destructive=Would this destroy or irreversibly alter production data?"
```

Ask several independent questions in one request when they share the same state:

```bash
cat ticket.txt |
  ai evaluate \
    --boolean "urgent=Does this require immediate human attention?" \
    --choice "route=Which team should own this?" \
    --choices "route=billing,support,security" \
    --score "impact=How severely is the customer blocked?" \
    --levels "impact=cosmetic,workaround exists,fully blocked"
```

Use a question file when labels contain commas, options need distinct
descriptions, or instructions are structured:

```json
{
  "route": {
    "type": "choice",
    "instructions": "Choose the single best owning team.",
    "criteria": {
      "billing": "Payments, invoices, charges, or refunds",
      "support": "Product help that is not security-related",
      "security": "Credential theft, abuse, or data exposure"
    }
  },
  "impact": {
    "type": "score",
    "instructions": "Score how severely the user is blocked.",
    "criteria": ["Cosmetic", "Workaround exists", "No workaround"]
  }
}
```

```bash
ai evaluate --questions questions.json < state.json
```

Useful options:

```text
--boolean id=question
--choice id=question      --choices id=a,b,c
--score id=question       --levels id=low,medium,high
--questions path.json
--input auto|text|json
--provider-options path.json
--max-retries n
--timeout seconds
-m typesafe-ai/jev
```

`--input auto` preserves a complete JSON object or array; otherwise it sends
text. Empty input and binary input fail. Convert JSONL to one array explicitly
with `jq -s .` when that is the intended shared state.

## Interpret results

- Boolean: `probability` is P(true), from 0 to 1. A valid false or uncertain
  result still exits 0.
- Choice: `choice` is one declared key; `probabilities` may contain the option
  distribution.
- Score: `score` is the probability-weighted position over zero-based ordered
  levels, not a percentage; `probabilities` may contain the distribution.
- Missing distributions or confidence must remain missing. Do not invent them.

Apply policy separately, for example:

```bash
ai evaluate --boolean "phish=Is this a phishing attempt?" < message.txt |
  jq -e '.answers.phish.probability >= 0.95'
```

Here `jq`, not Jev or `ai evaluate`, owns the threshold and pipeline exit status.

## Write effective questions

- Ask one observable property per question.
- Define every choice and ordered score level precisely.
- Put all needed context in the shared state; question IDs are code identifiers,
  not instructions.
- Questions in one call are independent. Use a later call when one decision needs
  an earlier answer or newly retrieved state.
- Establish thresholds with labeled examples. Route uncertain or high-impact
  cases to deterministic checks or human review.

Current references:

- [ai-cli Evaluate](https://ai-cli.dev/docs/evaluate)
- [Jev on Vercel AI Gateway](https://vercel.com/ai-gateway/models/jev)
- [TypeSafe AI introduction to Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
