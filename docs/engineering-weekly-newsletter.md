# Engineering Weekly Newsletter

`engineering-weekly-newsletter` is a public-news research and writing workflow for engineering leaders and senior practitioners. It is not a generic status-template generator and does not require a company vault.

## What it does

- Resolves an exact reporting window and marks a partial current day.
- Researches first-party announcements, independent context, and practitioner discussion.
- Accepts optional notes, links, exports, or source bundles as a separate evidence lane.
- Distinguishes announcement, release, general availability, adoption, and measured outcome.
- Rejects stale stories unless an in-window material change occurred.
- Produces a concise Markdown newsletter with linked sources and a review checklist.
- Validates the final Markdown deterministically before calling it review-ready.

## Example prompts

```text
Research the most important software-engineering news from the last seven days and draft a three-minute weekly newsletter for engineering leaders.
```

```text
Create a developer-focused weekly brief for August 3 through August 9, 2026. Prioritize infrastructure, security, open source, and developer tooling.
```

```text
Turn these links and notes into a review-ready engineering newsletter. Verify public claims, preserve disagreements, and list anything unresolved.
```

## Research model

The plugin uses three evidence lanes:

1. **First-party evidence** for what was announced, released, changed, priced, specified, or measured.
2. **Independent context** for significance, comparison, limitations, and impact.
3. **Community evidence** for attributed practitioner reaction, friction, and emerging questions.

Community engagement is treated as attention rather than proof. If the optional `$last30days` skill is installed, the workflow prefers it for recent community research; otherwise it uses the host's available public-web research and discloses reduced coverage.

## Output contract

Every review-ready newsletter includes:

- the exact inclusive reporting window;
- lead stories with **What changed**, **Why it matters**, and linked sources;
- explicit coverage or degraded-lane disclosure;
- a review checklist, including a clear `None` when all items are resolved; and
- a passing strict validator result.

The template is adaptable. Empty optional sections should be omitted instead of padded.

## Maintainer notes

The shared Agent Skill is under:

```text
plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/
```

Keep operational instructions required at runtime inside that folder. Keep release notes, repository contribution guidance, architecture commentary, and long-form user documentation in the repository-level `docs/` directory.
