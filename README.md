# 🔌 AI Plugins

![David Asaf plugs AI into a computer in a retro-futurist illustration](assets/ai-plugins-banner.png)

Portable, evidence-grounded plugins for AI-assisted research and publishing workflows.

This repository is a dual-format marketplace for OpenAI Codex/ChatGPT and Claude Code. Each ecosystem has its own thin manifest, while the Agent Skill workflow, references, scripts, templates, and examples remain single-source.

## 🧩 Available plugins

### 📰 Engineering Weekly Newsletter

Researches an explicit public-news window and produces a concise, review-ready engineering newsletter. It qualifies evidence, separates announcement from release and adoption, links claims to sources, excludes stale repetition, and surfaces unresolved claims instead of inventing certainty.

[Read the plugin guide](docs/engineering-weekly-newsletter.md)

## 🚀 Install

This repository is published as `davideasaf/ai-plugins`.

### 🤖 Codex and ChatGPT

Add the marketplace from a terminal:

```bash
codex plugin marketplace add davideasaf/ai-plugins
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **AI Plugins**, and install **Engineering Weekly Newsletter**.

For local testing from this checkout:

```bash
codex plugin marketplace add /absolute/path/to/ai-plugins
```

### 🟠 Claude Code

Add the marketplace and install the plugin:

```text
/plugin marketplace add davideasaf/ai-plugins
/plugin install engineering-weekly-newsletter@ai-plugins
```

For local testing, replace `davideasaf/ai-plugins` with the absolute path to this checkout.

### 🗞️ Optional: richer community research

The newsletter works without additional plugins. For broader Reddit, X, YouTube, Hacker News, GitHub, and other recent community signals, install the independently maintained [`last30days`](https://github.com/mvanhorn/last30days-skill) skill.

It is intentionally **not bundled or auto-installed**. This avoids shipping a stale fork, keeps credentials and source setup under the user's control, and preserves a usable public-web fallback.

For Codex and other Agent Skills hosts:

```bash
npx skills add mvanhorn/last30days-skill -g -a codex
```

For Claude Code:

```text
/plugin marketplace add mvanhorn/last30days-skill
/plugin install last30days
```

| Community capability | With `last30days` | Without `last30days` |
|---|---|---|
| Recent practitioner signal | Multi-source skill coverage and engagement context | Host public-web search |
| Newsletter generation | Full workflow | Full workflow |
| Handoff | Reports actual source coverage | Marks community coverage as degraded |

The newsletter treats engagement as attention rather than proof in either mode.

## 🔄 Update

Refresh the OpenAI marketplace snapshot:

```bash
codex plugin marketplace upgrade ai-plugins
```

Then restart the ChatGPT desktop app and reinstall or update **Engineering Weekly Newsletter** from the **AI Plugins** source so its cached installed copy is refreshed.

Refresh and update in Claude Code:

```text
/plugin marketplace update ai-plugins
```

```bash
claude plugin update engineering-weekly-newsletter@ai-plugins
```

Update the optional `last30days` companion separately:

```bash
npx skills update last30days -g
```

```bash
claude plugin update last30days@last30days-skill
```

## 🧠 Why two manifests?

The reusable capability is an Agent Skill under `skills/`. OpenAI and Claude Code both understand that core layout, but their packaging metadata is different:

| Concern | OpenAI Codex/ChatGPT | Claude Code |
|---|---|---|
| Repository catalog | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json` |
| Plugin manifest | `.codex-plugin/plugin.json` | `.claude-plugin/plugin.json` |
| Shared workflow | `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` |

The repository therefore unifies the plugin content, not the platform manifests. Platform-specific capabilities can be added later without contaminating the shared skill core.

## 🗂️ Repository layout

```text
ai-plugins/
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
├── docs/
├── plugins/
│   └── engineering-weekly-newsletter/
│       ├── .codex-plugin/plugin.json
│       ├── .claude-plugin/plugin.json
│       └── skills/engineering-weekly-newsletter/
└── README.md
```

Human-facing documentation lives at the repository root and in `docs/`. Runtime instructions stay beside the skill in `references/` and `assets/`. This keeps the installed plugin compact and keeps GitHub documentation useful without asking the model to load maintainer material.

## ✅ Validate

```bash
python3 -m unittest discover \
  -s plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/tests

python3 \
  plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/scripts/validate_newsletter.py \
  plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/examples/expected-newsletter.md \
  --strict

claude plugin validate .
claude plugin validate ./plugins/engineering-weekly-newsletter
```

OpenAI authoring validation is run with the official `plugin-creator` and `skill-creator` tooling before release.

Maintainers should follow the [release checklist](docs/releasing.md) so OpenAI and Claude metadata remain synchronized.

## 🔒 Safety and privacy

The newsletter plugin researches public information by default. User-provided private material stays a separate local evidence lane and must not be sent to public research tools without explicit authorization. The plugin never sends, publishes, schedules, subscribes, posts, or mutates external systems without authorization for that exact action.

## 📄 License

[MIT](LICENSE)
