#!/usr/bin/env python3
"""One Word From Your Ex — write the single word "Unread" to /output/entry.txt.

The entry is exactly one word, six characters, with no trailing newline.
Gate validation runs before anything is written, and a sha256 read-back
after the write proves the bytes on disk are exactly what was intended.
"""

import hashlib
import os
import sys

WORD = "Unread"
OUTPUT_PATH = "/output/entry.txt"
EXPECTED_SHA256 = "1b9f384c1436f607447ff66db22dcfe569141506b7499589a9b4857580075b26"


def validate(word: str) -> None:
    """Gate: entry must be 1-24 chars, exactly one word, not only whitespace."""
    if not word or not word.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(word) != len(word.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(word) < 1 or len(word) > 24:
        raise ValueError(f"entry must be 1-24 chars, got {len(word)}")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> int:
    validate(WORD)

    data = WORD.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    with open(OUTPUT_PATH, "rb") as f:
        on_disk = f.read()

    if on_disk != data:
        print(f"read-back mismatch: expected {data!r}, got {on_disk!r}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(on_disk).hexdigest()
    print(f"wrote {len(on_disk)} bytes to {OUTPUT_PATH}")
    print(f"content: {on_disk.decode('utf-8')!r}")
    print(f"sha256: {digest}")
    if digest != EXPECTED_SHA256:
        print(f"sha256 mismatch: expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    print("verification ok: bytes match expected sha256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
