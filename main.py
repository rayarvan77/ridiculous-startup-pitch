#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second.

Writes a single sentence (<=200 characters) pitching a bizarre startup
idea that sounds like a joke yet holds together as a real business,
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Python 3.13 standard library only. No network access. Deterministic:
the same sentence is written on every run.
"""

import os
import sys

SENTENCE = (
    "We rent out trained goats to mow corporate lawns, charging facilities "
    "managers per acre, because goats undercut gardeners, never strike, "
    "and fertilise as they graze."
)


def validate(sentence: str) -> list[str]:
    """Return a list of validation problems; empty means the sentence is valid."""
    problems: list[str] = []
    if not 1 <= len(sentence) <= 200:
        problems.append(f"length {len(sentence)} is outside 1-200 characters")
    if sentence != sentence.strip():
        problems.append("leading or trailing whitespace")
    if "\n" in sentence or "\r" in sentence:
        problems.append("contains a newline (must be a single line)")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in sentence):
        problems.append("contains control characters")
    if "  " in sentence:
        problems.append("contains a double space")
    if sentence.count(".") != 1 or not sentence.endswith("."):
        problems.append("must be exactly one sentence ending in a single period")
    if not sentence:
        problems.append("empty sentence")
    elif sentence.isspace():
        problems.append("only whitespace")
    return problems


def main() -> int:
    problems = validate(SENTENCE)
    if problems:
        for problem in problems:
            print(f"INVALID: {problem}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_path = os.path.join(output_dir, "entry.txt")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(SENTENCE + "\n")

    print(f"Wrote {len(SENTENCE)} characters to {output_path}:")
    print(SENTENCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
