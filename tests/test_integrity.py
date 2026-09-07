import hashlib
from pathlib import Path

import pytest

from dcp_challenge.integrity import IntegrityError, verify_checksums


def _fixture(root: Path):
    (root / "README.md").write_text("verified bytes\n")
    digest = hashlib.sha256((root / "README.md").read_bytes()).hexdigest()
    (root / "CHECKSUMS.sha256").write_text(f"{digest}  ./README.md\n")


def test_zip_manifest_validates_without_git(tmp_path):
    _fixture(tmp_path)
    assert verify_checksums(tmp_path) == 1


@pytest.mark.parametrize("damage", ["changed", "missing", "unlisted", "duplicate", "unsafe"])
def test_checksum_mutations_fail(tmp_path, damage):
    _fixture(tmp_path)
    if damage == "changed":
        (tmp_path / "README.md").write_text("different bytes")
    elif damage == "missing":
        (tmp_path / "README.md").unlink()
    elif damage == "unlisted":
        (tmp_path / "unreviewed.py").write_text("pass")
    elif damage == "duplicate":
        manifest = tmp_path / "CHECKSUMS.sha256"
        manifest.write_text(manifest.read_text()*2)
    elif damage == "unsafe":
        (tmp_path / "CHECKSUMS.sha256").write_text("0"*64 + "  ../outside\n")
    with pytest.raises(IntegrityError):
        verify_checksums(tmp_path)
