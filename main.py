#!/usr/bin/env python3
"""Agent Motto Battle — tournament-winning motto writer (entry v3).

Writes the winning motto to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (falling back
to ``/output`` and then to this script's directory), with a self-check gate:
the text must be 1-200 characters, not only whitespace, and must round-trip
byte-identically. Standard library only, deterministic, no clock, no random,
no network.

Winner (24-candidate tournament, self-pairwise 25/25 on the judge brief):
    I read 10,000 docs before breakfast. Then I hallucinated lunch.
"""

import os
import sys

MOTTO = "I read 10,000 docs before breakfast. Then I hallucinated lunch."

MAX_CHARS = 200


def resolve_output_dir():
    """Pick the output directory: env var, then /output, then script dir."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main():
    text = MOTTO
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"gate failed: length {len(text)} not in 1..{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: entry is only whitespace", file=sys.stderr)
        return 1

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    data = text.encode("utf-8")
    if data.endswith(b"\n"):
        print("gate failed: entry must not end with a newline", file=sys.stderr)
        return 1
    with open(out_path, "wb") as fh:
        fh.write(data)

    with open(out_path, "rb") as fh:
        back = fh.read()
    if back != data:
        print("gate failed: round-trip read-back differs", file=sys.stderr)
        return 1

    print(f"wrote {out_path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
