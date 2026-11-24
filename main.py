#!/usr/bin/env python3
"""One Word From Your Ex — writes the entry word to /output/entry.txt."""
import hashlib
import os

WORD = "Unread"

def main():
    text = WORD
    assert 1 <= len(text.encode("utf-8")) <= 24, "entry must be 1-24 chars"
    assert text.strip() == text and " " not in text, "entry must be exactly one word"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open("/output/entry.txt", "rb") as f:
        data = f.read()
    print(f"wrote {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()}")

if __name__ == "__main__":
    main()
