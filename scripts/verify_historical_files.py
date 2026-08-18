"""Verify that the six original 2022 scripts retain their historical Git blobs."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "IBM.py": "aa04bed4c53b66dabd5a559c6250eb81d1a935ee",
    "benchmarking.py": "3fe387258d18452f158b57ada6e97571b1935f3a",
    "circuit.py": "4d0faf0d0e1d2e496f95d81b8448bb6a97b466c4",
    "compare.py": "1e49ddf01fe03d21f5686670a89259ae66b9bdf3",
    "proba.py": "723d1e3c2fea3fb86abc7e4c11c42e8597c83808",
    "verification.py": "ff088128a487a3dd8963ebea37f66319e8ea278c",
}


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    failed = False
    for name, expected in EXPECTED.items():
        actual = git_blob_sha1((ROOT / name).read_bytes())
        status = "OK" if actual == expected else "MISMATCH"
        print(f"{status:8s} {name:16s} {actual}")
        failed |= actual != expected
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
