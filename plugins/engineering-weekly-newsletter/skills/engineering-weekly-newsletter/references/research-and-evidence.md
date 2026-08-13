# Research and evidence

## Default editorial desks

Search these as open categories, not a closed vendor list:

- developer tools and AI-assisted engineering;
- software architecture, platforms, APIs, and data systems;
- cloud, infrastructure, performance, and observability;
- reliability, security, privacy, and standards;
- open source, research, frameworks, and programming languages;
- engineering leadership, developer experience, and delivery practice.

## Evidence lanes

1. **First-party facts:** release notes, documentation, repositories, papers, standards, official advisories, and vendor announcements. Use these for what shipped, when, where, and under what limitations.
2. **Independent context:** technically credible reporting, analysis, benchmarks, and comparisons. Use these for consequence, trade-offs, and disagreement. Inspect methodology before repeating a number.
3. **Community signal:** practitioner posts, discussions, videos, comments, and engagement. Prefer `$last30days` when installed. Attribute the speaker or community and never promote reaction into fact.

## Evidence ledger

Record one row per candidate claim:

| Field | Meaning |
|---|---|
| Event | Underlying change, not headline |
| Event date | Date the change occurred |
| Source | Exact URL and publisher or speaker |
| Claim | Atomic statement supported by the source |
| Evidence class | first-party, corroborated, attributed reporting, community signal, analysis, or prediction |
| Publication state | proposed, announced, released, generally available, adopted, or measured |
| Scope | Platform, region, version, sample, or audience limit |
| Confidence | high, medium, or low with reason |
| Open question | Missing proof needed for stronger wording |

## Publication states

- **Proposed:** design, roadmap, draft, experiment, or prediction. No delivery claim.
- **Announced:** an identified party publicly committed to or described a change. Not proof of release.
- **Released:** an artifact, version, feature, or code change is available in a defined channel. Not proof of general availability or use.
- **Generally available:** the provider documents broad production availability and applicable limits. Not proof of adoption.
- **Adopted:** a named user or measured population used the capability. Self-reported adoption remains attributed.
- **Measured:** a defined metric, population, period, baseline, and method support the outcome. A benchmark is not customer or business impact unless designed to measure it.

Never use a commit as release proof, a release as adoption proof, or adoption as outcome proof.

## Window and selection

- Require an in-window catalyst for every story. An older topic qualifies only when a new release, paper, decision, incident, benchmark, or substantive discussion occurred inside the window.
- Record the final day as partial when applicable.
- Deduplicate by underlying event across sources.
- Prefer the latest authoritative correction when sources conflict. If authority or chronology does not resolve the conflict, omit the claim and add it to review.
- Score candidates by source quality, engineering consequence, audience relevance, novelty, cross-source confirmation, and clarity of practical implication.
- Use engagement only to rank community attention. It cannot verify the underlying claim.
- Drop stale repetition, promotional copy with no material change, isolated low-signal posts, and stories outside the requested audience.

## Source posture

- Link directly to the supporting page, not a search result.
- Prefer primary sources for exact dates, versions, availability, pricing, licenses, security, and benchmark methods.
- Attribute reporting that is not independently confirmed.
- Preserve uncertainty and material disagreement.
- Treat missing or failed research lanes as degraded coverage, not evidence that nothing happened.
- Keep private local inputs separate from public queries. Never paste confidential text into a search or third-party research tool without explicit authorization.
