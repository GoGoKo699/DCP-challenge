from pathlib import Path
import hashlib

EXPECTED = {
    "IBM.py": "aa04bed4c53b66dabd5a559c6250eb81d1a935ee",
    "benchmarking.py": "3fe387258d18452f158b57ada6e97571b1935f3a",
    "circuit.py": "4d0faf0d0e1d2e496f95d81b8448bb6a97b466c4",
    "compare.py": "1e49ddf01fe03d21f5686670a89259ae66b9bdf3",
    "proba.py": "723d1e3c2fea3fb86abc7e4c11c42e8597c83808",
    "verification.py": "ff088128a487a3dd8963ebea37f66319e8ea278c",
}
ROOT = Path(__file__).resolve().parents[1]


def test_original_scripts_match_historical_git_blobs() -> None:
    for name, expected in EXPECTED.items():
        data = (ROOT / name).read_bytes()
        actual = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
        assert actual == expected
