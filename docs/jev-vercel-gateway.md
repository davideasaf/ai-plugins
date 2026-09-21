# ⚖️ Jev via Vercel AI Gateway

Use TypeSafe AI's Jev for fast, typed decisions when the possible answers are known in advance. The plugin supports Boolean questions, fixed choices, and ordered scores from shell pipelines or application code.

## Good fits

- Route a support request to one of a fixed set of teams.
- Flag whether a deployment plan appears destructive.
- Score customer impact across ordered severity levels.
- Add a cheap decision layer before a larger generative model.

Jev is not intended for open-ended prose, code generation, or discovering labels that were not declared before the call.

## Requirements

- Node.js 22 or later.
- `ai-cli` 0.5.1 or later for terminal use.
- A Vercel AI Gateway key available as `AI_GATEWAY_API_KEY`.

Keep the key in the environment. Do not put it in prompts, source files, command arguments, logs, or the plugin itself.

## Examples

Evaluate a Boolean question from stdin:

```bash
printf '%s\n' 'The migration drops the production customer table.' |
  ai evaluate --boolean "destructive=Would this destroy or irreversibly alter production data?"
```

Choose a route and score impact in one request:

```bash
cat ticket.txt |
  ai evaluate \
    --choice "route=Which team should own this?" \
    --choices "route=billing,support,security" \
    --score "impact=How severely is the customer blocked?" \
    --levels "impact=cosmetic,workaround exists,fully blocked"
```

For application integration, invoke the plugin and ask it to add a typed Jev decision to the relevant service or script. It uses the AI SDK evaluation API and keeps thresholds, fallbacks, review queues, and mutations outside the model call.

## Safety model

Typed output limits the shape of an answer; it does not make the judgment infallible. Calibrate thresholds on representative labeled data, preserve missing confidence instead of inventing it, and require deterministic validation or human review for high-impact actions.
