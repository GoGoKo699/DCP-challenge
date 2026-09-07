"""Verify all tracked file checksums and manifest coverage."""
from pathlib import Path

from dcp_challenge.integrity import verify_checksums

if __name__ == "__main__":
    count = verify_checksums(Path(__file__).resolve().parents[1])
    print(f"Checksum verification passed: {count} files; complete manifest coverage.")
