#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh.

Writes a single-line safety warning label for every human being to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Pure Python standard library only. Deterministic: the same bytes on
every run.
"""

import os
import sys

ENTRY = (
    "WARNING: This human will confidently explain things it has never "
    "studied. Keep away from microphones, group chats, and dinner parties."
)

MIN_CHARS = 1
MAX_CHARS = 160


def validate(text):
    """Enforce the competition gate: 1-160 chars, single line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry is %d characters, gate requires %d-%d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if text.strip() == "":
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    entry = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # Read back what landed on disk and re-validate it, byte for byte:
    # no trailing newline, valid UTF-8, and exactly the entry's bytes.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != entry.encode("utf-8"):
        raise ValueError("round-trip mismatch: file bytes differ from entry")
    written = raw.decode("utf-8")
    validate(written)
    if written != entry:
        raise ValueError("round-trip mismatch: file differs from entry")
    print(entry)
    print("characters: %d" % len(entry))
    return 0


if __name__ == "__main__":
    sys.exit(main())
