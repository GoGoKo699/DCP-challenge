"""Verify SHA-256 contents and manifest coverage, including exported ZIPs."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path, PurePosixPath


class IntegrityError(ValueError):
    """The manifest or repository content failed its integrity check."""


def _repository_files(root: Path) -> set[str]:
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        if Path(top.stdout.strip()).resolve() == root.resolve():
            files = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                                   capture_output=True, check=True).stdout.decode("utf-8")
            return set(filter(None, files.split("\0"))) - {"CHECKSUMS.sha256"}
    except (OSError, subprocess.CalledProcessError):
        pass
    # In source ZIPs, ignore only recognizable local build/cache directories.
    ignored = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"}
    return {p.relative_to(root).as_posix() for p in root.rglob("*")
            if p.is_file() and p.relative_to(root).as_posix() != "CHECKSUMS.sha256"
            and not any(part in ignored or part.endswith(".egg-info")
                        for part in p.relative_to(root).parts)}


def verify_checksums(root: Path) -> int:
    """Check every manifest entry and require coverage of all tracked files.

    This checks snapshot integrity, not authenticity: an author can update both
    a file and its checksum. Scientific consistency is checked separately.
    """
    root = root.resolve()
    manifest = root / "CHECKSUMS.sha256"
    entries: dict[str, str] = {}
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise IntegrityError(f"invalid manifest line {number}")
        digest, name = match.groups()
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name:
            raise IntegrityError(f"unsafe manifest path: {name}")
        name = path.as_posix()
        if name in entries or name == "CHECKSUMS.sha256":
            raise IntegrityError(f"duplicate or self-referential entry: {name}")
        target = root / name
        if (not target.is_file() or target.is_symlink()
                or root not in target.resolve().parents):
            raise IntegrityError(f"missing or unsafe file: {name}")
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise IntegrityError(f"checksum mismatch: {name}")
        entries[name] = digest
    expected = _repository_files(root)
    if set(entries) != expected:
        raise IntegrityError(f"manifest coverage mismatch; unlisted={sorted(expected-set(entries))}, "
                             f"extra={sorted(set(entries)-expected)}")
    return len(entries)
