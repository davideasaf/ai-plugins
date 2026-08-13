#!/usr/bin/env python3
"""Validate a Markdown Engineering Weekly Newsletter."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
import sys


TITLE_RE = re.compile(r"^#\s+Engineering Weekly Newsletter\s*$", re.MULTILINE)
WINDOW_RE = re.compile(
    r"\*\*Reporting window:\*\*\s*"
    r"(?P<start>\d{4}-\d{2}-\d{2})\s+to\s+"
    r"(?P<end>\d{4}-\d{2}-\d{2})\s*\(inclusive\)",
    re.IGNORECASE,
)
LEAD_SECTION_RE = re.compile(
    r"^##\s+Lead stories\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
STORY_RE = re.compile(
    r"^###\s+(?P<title>.+?)\s*$\n(?P<body>.*?)(?=^###\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
LINK_RE = re.compile(r"\[[^\]\n]+\]\(https://[^)\s]+\)")
REVIEW_HEADING_RE = re.compile(r"^##\s+Review checklist\s*$", re.IGNORECASE | re.MULTILINE)
UNCHECKED_RE = re.compile(r"^\s*-\s*\[\s\]\s+\S", re.MULTILINE)
READY_RE = re.compile(r"\bready to (?:send|publish|post)\b", re.IGNORECASE)
TEMPLATE_RE = re.compile(
    r"\{\{[^}\n]+\}\}|\[(?:todo|tbd|replace|insert)[^\]\n]*\]|\b(?:TODO|TBD):",
    re.IGNORECASE,
)
EVIDENCE_LABEL_RE = re.compile(
    r"\[(?:first-party|corroborated|attributed|community signal|analysis|proposal|prediction|unknown)\]",
    re.IGNORECASE,
)
STATE_SHORTCUT_PATTERNS = (
    re.compile(
        r"\bannounced\s+(?:(?:and|means|therefore)\s+){1,2}(?:released|available|generally available)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\breleased\s+(?:and|means|therefore)\s+(?:adopted|measured)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bgenerally available\s+(?:and|means|therefore)\s+adopted\b", re.IGNORECASE),
    re.compile(r"\badopted\s+(?:and|means|therefore)\s+measured\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str


def validate_text(text: str) -> list[Diagnostic]:
    """Return deterministic structure, sourcing, and publication-state diagnostics."""

    diagnostics: list[Diagnostic] = []

    if not TITLE_RE.search(text):
        diagnostics.append(
            Diagnostic("ERROR", "document.title", "Missing '# Engineering Weekly Newsletter' title.")
        )

    window_match = WINDOW_RE.search(text)
    if not window_match:
        diagnostics.append(
            Diagnostic(
                "ERROR",
                "window.missing",
                "Add an inclusive ISO reporting window: YYYY-MM-DD to YYYY-MM-DD.",
            )
        )
    else:
        try:
            start = date.fromisoformat(window_match.group("start"))
            end = date.fromisoformat(window_match.group("end"))
        except ValueError:
            diagnostics.append(
                Diagnostic("ERROR", "window.invalid", "The reporting window contains an invalid date.")
            )
        else:
            if start > end:
                diagnostics.append(
                    Diagnostic(
                        "ERROR",
                        "window.reversed",
                        "The reporting-window start date is after the end date.",
                    )
                )

    lead_match = LEAD_SECTION_RE.search(text)
    stories = list(STORY_RE.finditer(lead_match.group("body"))) if lead_match else []
    if not stories:
        diagnostics.append(
            Diagnostic("ERROR", "story.missing", "Add at least one story under '## Lead stories'.")
        )
    for story in stories:
        title = story.group("title").strip()
        body = story.group("body")
        if not re.search(r"^\*\*What changed:\*\*\s+\S", body, re.MULTILINE):
            diagnostics.append(
                Diagnostic(
                    "ERROR", "story.what-changed", f"Story '{title}' is missing '**What changed:**'."
                )
            )
        if not re.search(r"^\*\*Why it matters:\*\*\s+\S", body, re.MULTILINE):
            diagnostics.append(
                Diagnostic(
                    "ERROR", "story.why-it-matters", f"Story '{title}' is missing '**Why it matters:**'."
                )
            )
        if not LINK_RE.search(body):
            diagnostics.append(
                Diagnostic(
                    "ERROR", "story.source-link", f"Story '{title}' needs an HTTPS Markdown source link."
                )
            )

    review_match = REVIEW_HEADING_RE.search(text)
    if not review_match:
        diagnostics.append(
            Diagnostic("ERROR", "review.missing", "Add a '## Review checklist' section.")
        )

    if TEMPLATE_RE.search(text):
        diagnostics.append(
            Diagnostic("ERROR", "template.unresolved", "Remove unresolved template markers.")
        )

    reader_copy = text[: review_match.start()] if review_match else text
    if EVIDENCE_LABEL_RE.search(reader_copy):
        diagnostics.append(
            Diagnostic(
                "ERROR",
                "copy.evidence-label",
                "Keep ledger labels out of reader-facing copy; express qualification naturally.",
            )
        )

    if any(pattern.search(reader_copy) for pattern in STATE_SHORTCUT_PATTERNS):
        diagnostics.append(
            Diagnostic(
                "ERROR",
                "state.shortcut",
                "Do not collapse announcement, release, availability, adoption, or measurement states.",
            )
        )

    if READY_RE.search(text) and UNCHECKED_RE.search(text):
        diagnostics.append(
            Diagnostic(
                "ERROR",
                "review.not-ready",
                "Do not claim the newsletter is ready while review items remain unchecked.",
            )
        )

    return diagnostics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Markdown newsletter to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as blocking errors (reserved for forward-compatible checks)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = args.markdown.read_text(encoding="utf-8")
    except OSError as error:
        print(f"ERROR file.read: {error}", file=sys.stderr)
        return 1

    diagnostics = validate_text(text)
    for diagnostic in diagnostics:
        print(f"{diagnostic.severity} {diagnostic.code}: {diagnostic.message}")

    blocking = [
        diagnostic
        for diagnostic in diagnostics
        if diagnostic.severity == "ERROR" or args.strict
    ]
    if blocking:
        return 1

    print("OK: engineering weekly newsletter passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
