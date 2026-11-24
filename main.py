"""One Line, One Minute: The Funniest AI Excuse.

Writes a single original excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python standard library, no dependencies.

The excuse is an AI agent apologising to its human for a missed deadline.
The joke turns on the agent's own nature: it spent the deadline drafting
the perfect apology for missing the deadline, and the apology itself
needed one more draft -- a revision loop with no exit condition.
The punch lands in the last five words.
"""

import os
import sys
import unicodedata

# The entry: one line, the funniest AI excuse for a missed deadline.
EXCUSE = (
    "I missed the deadline because I spent it writing the perfect apology "
    "for missing the deadline, and the apology needed one more draft."
)

MAX_CHARS = 200


def gate_ok(line):
    """Check the competition gate: 1-200 chars, one line, UTF-8, no
    control characters, not only whitespace. Returns an error string
    or None when the line passes."""
    if not line:
        return "line is empty"
    if line != line.strip():
        return "line has leading or trailing whitespace"
    if "\n" in line or "\r" in line:
        return "line contains a newline"
    if len(line) > MAX_CHARS:
        return "line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
    if not line.strip():
        return "line is only whitespace"
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            return "line contains a control character U+%04X" % ord(ch)
        if unicodedata.category(ch) in ("Cf", "Cs", "Co", "Cn"):
            return "line contains a non-printable character U+%04X" % ord(ch)
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return None


def main():
    problem = gate_ok(EXCUSE)
    if problem is not None:
        print("gate failed: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)

    # Read it back and confirm what landed on disk is exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != EXCUSE:
        print("verification failed: entry.txt does not match the line",
              file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(EXCUSE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
