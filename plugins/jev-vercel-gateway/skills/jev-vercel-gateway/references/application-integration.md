# Application integration

Read this reference when adding Jev to an application, system, service, or script.
The AI SDK evaluation API is experimental, so pin and test the `ai` package
version in production projects.

## TypeScript baseline

Install the current AI SDK:

```bash
npm install ai@latest
```

With `AI_GATEWAY_API_KEY` in the server environment, a `creator/model` string
automatically uses Vercel AI Gateway:

```ts
import { experimental_evaluate as evaluate } from 'ai';

const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: {
    subject: 'Urgent: verify your payroll account',
    body: 'Sign in at the linked page within one hour.',
    senderDomain: 'example.invalid',
  },
  questions: {
    phishing: {
      type: 'boolean',
      instructions: 'Is this likely a credential-phishing attempt?',
      criteria: {
        true: 'Attempts to obtain credentials through deception or impersonation',
        false: 'No evidence of credential theft or deceptive impersonation',
      },
    },
    route: {
      type: 'choice',
      instructions: 'Choose the review route.',
      criteria: {
        block: 'Strong phishing evidence; block and escalate',
        review: 'Ambiguous; require human review',
        allow: 'No meaningful phishing evidence',
      },
    },
    risk: {
      type: 'score',
      instructions: 'Score the potential security impact.',
      criteria: ['Low', 'Moderate', 'High', 'Critical'],
    },
  },
  maxRetries: 2,
});

console.log(result.answers.phishing.probability);
console.log(result.answers.route.choice);
console.log(result.answers.risk.score);
```

The result also includes usage, warnings, response metadata, optional rounding,
and optional provider metadata. Preserve absent optional fields rather than
synthesizing values.

## Decision boundary

Keep the model call and policy separate. This makes thresholds auditable and
lets tests exercise policy without spending Gateway credits:

```ts
export type ReviewAction = 'block' | 'review' | 'allow';

export function chooseAction(probability: number): ReviewAction {
  if (probability >= 0.98) return 'block';
  if (probability >= 0.6) return 'review';
  return 'allow';
}
```

Those numbers are examples, not defaults. Select them from labeled examples and
the costs of false positives and false negatives. High-impact actions should
usually require deterministic validation or human review in addition to a model
threshold.

## Reliability pattern

- Keep `AI_GATEWAY_API_KEY` server-side and read it from the environment.
- Give each question a stable ID; log the model ID, question-set version, latency,
  and result needed for audit, but not secrets or unnecessary source material.
- Apply an overall timeout with an `AbortSignal` appropriate to the caller.
- Treat timeouts, invalid answers, authentication failures, and provider errors
  as explicit failure paths. Do not silently reinterpret them as false or safe.
- Test question sets against representative labeled fixtures before production.
- Unit-test routing and thresholds without live calls; keep a small opt-in live
  smoke test for Gateway compatibility.

## CLI-to-code mapping

| `ai evaluate` | AI SDK `evaluate` |
| --- | --- |
| stdin | `state` |
| `--boolean id=...` | `{ type: 'boolean', instructions: ... }` |
| `--choice` + `--choices` | `{ type: 'choice', instructions, criteria }` |
| `--score` + `--levels` | `{ type: 'score', instructions, criteria }` |
| `--questions file.json` | `questions` |
| `--provider-options file.json` | `providerOptions` |
| `--max-retries` | `maxRetries` |

## Other runtimes

When TypeScript is not appropriate, call a small TypeScript service or execute
`ai evaluate` as a subprocess with JSON stdin/stdout. Avoid reconstructing an
undocumented REST payload: the evaluation interface is experimental and the AI
SDK/CLI carry its current schema and validation.
