#!/usr/bin/env python3
"""Make the Judge Laugh in One Line — entry program.

Writes a single original one-liner to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default /output). The sealed gate requires 1-200 characters of UTF-8
text, not only whitespace, on a single line.
"""

import os

ENTRY = "The dentist told me to stop grinding my teeth at night, so now I lie awake grinding my teeth over the bill instead."


def main() -> None:
    # Validate: one line, 1-200 chars, no control characters.
    if not 1 <= len(ENTRY) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(ENTRY)}")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in ENTRY):
        raise ValueError("entry contains control characters")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    ENTRY.encode("utf-8")  # raises if not valid UTF-8
    # The gate counts characters, but the file must also stay a sane
    # single-line UTF-8 payload: cap the byte length well above the
    # worst case for 200 chars (4 bytes each) as a sanity bound.
    if len(ENTRY.encode("utf-8")) > 800:
        raise ValueError("entry exceeds 800 UTF-8 bytes")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Round-trip verification: what is on disk must be byte-identical
    # to the validated entry, or the run has failed.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != ENTRY.encode("utf-8"):
        raise ValueError("round-trip check failed: entry.txt differs from ENTRY")
    print(f"wrote {len(ENTRY)} chars ({len(on_disk)} bytes) to {path}, verified")


if __name__ == "__main__":
    main()
