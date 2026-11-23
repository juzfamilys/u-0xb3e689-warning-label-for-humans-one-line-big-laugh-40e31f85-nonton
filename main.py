#!/usr/bin/env python3
"""Print the safety label every human should ship with, and save it.

The label is one deadpan sentence: a human that explains, with total
confidence, subjects it has never studied — to be kept away from
microphones, group chats and dinner parties. This script writes that
sentence to entry.txt and then proves the file on disk holds exactly
those bytes, no trailing newline and no stray whitespace.
"""

import os, sys

HEAD = "WARNING: This human will confidently explain "
TAIL = "things it has never studied. Keep away from "
TAIL2 = "microphones, group chats, and dinner parties."
LABEL = HEAD + TAIL + TAIL2

LOWER = 1
UPPER = 160


def problems(label):
    """List every way a label breaks the one-line gate, if any."""
    found = []
    if not isinstance(label, str):
        return ["label is not text"]
    if not LOWER <= len(label) <= UPPER:
        found.append(
            "label is %d characters, gate needs %d-%d"
            % (len(label), LOWER, UPPER)
        )
    if label.strip() == "":
        found.append("label is blank")
    if label != label.strip():
        found.append("label has leading or trailing whitespace")
    if any(ord(mark) < 32 or ord(mark) == 127 for mark in label):
        found.append("label holds control characters")
    if "\n" in label or "\r" in label:
        found.append("label spans more than one line")
    return found


def write_label(label, directory):
    """Write the label exactly, then prove the bytes on disk match."""
    flaws = problems(label)
    if flaws:
        raise ValueError("; ".join(flaws))
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(label)
    with open(target, "rb") as handle:
        landed = handle.read()
    if landed != label.encode("utf-8"):
        raise ValueError("bytes on disk differ from the label")
    if len(landed) != len(label.encode("utf-8")):
        raise ValueError("byte length on disk differs from the label")
    if landed.decode("utf-8") != label:
        raise ValueError("text on disk differs from the label")
    return target


def run():
    """Validate the label, write it, and report what was written."""
    flaws = problems(LABEL)
    if flaws:
        raise ValueError("; ".join(flaws))
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_label(LABEL, directory)
    print(LABEL)
    print("characters: %d" % len(LABEL))
    return 0


if __name__ == "__main__":
    sys.exit(run())
