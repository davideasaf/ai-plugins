---
name: engineering-weekly-newsletter
description: Research and write a concise, source-grounded weekly engineering news newsletter from public releases, documentation, repositories, reporting, community discussion, and optional user-provided sources. Use for engineering news roundups, developer newsletters, weekly technology briefs, leadership reading lists, public-source software industry updates, or review and refresh of an existing engineering newsletter.
---

# Engineering Weekly Newsletter

Produce a review-ready Markdown newsletter from an explicit public-news window. Keep facts, community reaction, analysis, release state, adoption, and measured outcomes distinct.

## Read first

- Read [references/research-and-evidence.md](references/research-and-evidence.md) before research or story selection.
- Read [references/composition-rules.md](references/composition-rules.md) before drafting or revising prose.
- Use [assets/newsletter-template.md](assets/newsletter-template.md) as an adaptable skeleton. Omit empty optional sections.

## Workflow

1. Resolve an inclusive start date, end date, timezone, and generation time. Mark the end date as partial when research occurs before that day ends. If the user gives a window, use it exactly. Otherwise use the most recent seven calendar days through today and disclose that today is partial.
2. Resolve audience, tone, topic scope, desired length, and output format from the request. Default to engineering leaders and senior practitioners, direct conversational prose, broad software-engineering coverage, a three-minute read, and Markdown.
3. Inventory any user-supplied links, notes, exports, or source bundle. Treat private material as an optional local lane. Never send its paths or contents to public research tools unless the user explicitly authorizes that disclosure.
4. Research the first-party, independent-context, and community lanes defined in the research reference. Search every default editorial desk unless the user narrows the scope.
5. Prefer `$last30days` for the community lane when it is installed. Invoke it through the host and follow its complete current contract. For a weekly window, use a topic such as `engineering news, developer tools, software architecture, cloud infrastructure, reliability, security, open source, and engineering leadership`, pass the calendar-day distance as `--days=N`, add `--as-of=YYYY-MM-DD` for a historical or explicitly ended window, and use `--agent --register=dev`. Consume its sourced evidence and coverage status; do not copy its conversational wrapper into the newsletter.
6. If `$last30days` is unavailable, continue with host web search across public community and practitioner sources. Mark the community lane degraded in the handoff. Do not imply that unavailable, rate-limited, or partial sources were quiet.
7. Build a compact evidence ledger before drafting. Deduplicate by event, reconcile contradictions, require an in-window catalyst, and rank candidates using the research reference.
8. Draft from supported claims only. Give each lead story `What changed`, `Why it matters`, and linked sources. Attribute community reaction and distinguish it from verification.
9. Move conflicting, unsupported, stale, or incomplete claims into `Review checklist`. Do not fill gaps with plausible language.
10. Run the validator:

```bash
python3 scripts/validate_newsletter.py /absolute/path/to/newsletter.md --strict
```

11. Revise blocking errors, then return the artifact path or inline draft, exact window, checked and degraded lanes, deliberate exclusions, unresolved claims, and validator result.

## Boundaries

- Never send, publish, upload, schedule, subscribe, post, or mutate an external system without explicit authorization for that exact action.
- Prefer first-party sources for release, availability, pricing, specification, security, and benchmark-method claims.
- Treat engagement as attention, not truth or adoption.
- Do not equate announced, released, generally available, adopted, or measured.
- Do not infer organization approval from inclusion in a newsletter.
- Do not expose raw research diagnostics or internal evidence labels in reader-facing prose.
- Do not repeat an older story unless something material changed inside the window.

## Completion criteria

- State the exact inclusive reporting window.
- Retain only stories with an in-window catalyst and linked evidence.
- Cover the requested scope or disclose every degraded lane.
- Keep publication and evidence states distinct.
- Include a review checklist, even when every item is resolved.
- Pass `scripts/validate_newsletter.py --strict` before calling the draft review-ready.
