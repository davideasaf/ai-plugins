"""Tests for the Engineering Weekly Newsletter validator."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_newsletter.py"
SPEC = importlib.util.spec_from_file_location("validate_newsletter", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


VALID_NEWSLETTER = """\
# Engineering Weekly Newsletter

**Reporting window:** 2026-08-03 to 2026-08-09 (inclusive)
**Audience:** Engineering leaders and senior practitioners

## This week in one sentence

Tooling moved faster than adoption evidence: two releases changed developer workflows, while measured production outcomes remained limited.

## Lead stories

### Northstar ships deterministic build caching

**What changed:** Northstar released build caching in version 2.4 on 2026-08-06. The vendor documents Linux and macOS support.

**Why it matters:** Teams can test whether repeat builds become faster without treating the release as proof of production adoption.

**Sources:** [Northstar release notes](https://example.com/northstar/releases/2.4), [Independent benchmark](https://example.org/northstar-benchmark)

### RiverDB publishes its failover design

**What changed:** RiverDB published a failover design proposal on 2026-08-07. Implementation is not yet released.

**Why it matters:** Platform teams can review the trade-offs now, but should not plan against availability until a release is confirmed.

**Sources:** [RiverDB design proposal](https://example.com/riverdb/design), [Maintainer discussion](https://community.example.org/riverdb-failover)

## What engineering leaders should ask

- Which build workloads should we benchmark before considering rollout?
- Do our recovery requirements match RiverDB's proposed trade-offs?

## Watchlist

- RiverDB failover availability remains unconfirmed.

## Review checklist

- [x] Every retained story has an in-window catalyst and linked source.
- [x] Announced, released, available, adopted, and measured states remain distinct.
- [ ] Confirm whether the RiverDB maintainers set a target release date.
"""


def codes(text: str) -> set[str]:
    return {diagnostic.code for diagnostic in validator.validate_text(text)}


class TestValidateText(unittest.TestCase):
    def test_accepts_source_grounded_newsletter_with_open_review_item(self):
        self.assertEqual([], validator.validate_text(VALID_NEWSLETTER))

    def test_requires_explicit_reporting_window(self):
        text = VALID_NEWSLETTER.replace(
            "**Reporting window:** 2026-08-03 to 2026-08-09 (inclusive)\n", ""
        )
        self.assertIn("window.missing", codes(text))

    def test_rejects_reversed_reporting_window(self):
        text = VALID_NEWSLETTER.replace("2026-08-03 to 2026-08-09", "2026-08-10 to 2026-08-09")
        self.assertIn("window.reversed", codes(text))

    def test_requires_story_source_link(self):
        text = VALID_NEWSLETTER.replace(
            "[Northstar release notes](https://example.com/northstar/releases/2.4), "
            "[Independent benchmark](https://example.org/northstar-benchmark)",
            "Northstar release notes and independent benchmark",
        )
        self.assertIn("story.source-link", codes(text))

    def test_requires_what_changed_in_every_story(self):
        text = VALID_NEWSLETTER.replace("**What changed:** Northstar", "Northstar")
        self.assertIn("story.what-changed", codes(text))

    def test_requires_why_it_matters_in_every_story(self):
        text = VALID_NEWSLETTER.replace("**Why it matters:** Teams", "Teams")
        self.assertIn("story.why-it-matters", codes(text))

    def test_rejects_unresolved_template_marker(self):
        text = VALID_NEWSLETTER.replace("## This week in one sentence", "## This week in one sentence\n\n{{weekly thesis}}")
        self.assertIn("template.unresolved", codes(text))

    def test_rejects_internal_evidence_labels_in_reader_copy(self):
        text = VALID_NEWSLETTER.replace("Northstar released", "[first-party] Northstar released")
        self.assertIn("copy.evidence-label", codes(text))

    def test_rejects_publication_state_shortcut(self):
        text = VALID_NEWSLETTER.replace(
            "The vendor documents Linux and macOS support.",
            "It was announced and therefore generally available.",
        )
        self.assertIn("state.shortcut", codes(text))

    def test_requires_review_checklist(self):
        text = VALID_NEWSLETTER.split("## Review checklist", 1)[0]
        self.assertIn("review.missing", codes(text))

    def test_rejects_ready_to_publish_claim_with_open_items(self):
        text = VALID_NEWSLETTER.replace("## Review checklist", "Ready to publish.\n\n## Review checklist")
        self.assertIn("review.not-ready", codes(text))


class TestCli(unittest.TestCase):
    def test_returns_zero_for_valid_newsletter(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "newsletter.md"
            target.write_text(VALID_NEWSLETTER, encoding="utf-8")
            self.assertEqual(0, validator.main([str(target), "--strict"]))

    def test_returns_one_for_invalid_newsletter(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "newsletter.md"
            target.write_text("# Engineering Weekly Newsletter\n", encoding="utf-8")
            self.assertEqual(1, validator.main([str(target)]))


if __name__ == "__main__":
    unittest.main()
