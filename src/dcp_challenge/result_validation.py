"""Strict, read-only validation of every field in the committed result records.

The expected values are generated without reading the result files. Frozen
Monte Carlo counts are checked as archived evidence, not newly sampled data.
"""
from __future__ import annotations

import csv
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

from .reference_results import build_results


class ValidationError(ValueError):
    """A result is missing, malformed, or inconsistent with its reference."""


@lru_cache(maxsize=1)
def _expected_results() -> dict[str, Any]:
    return build_results()


def compare_records(actual: Any, expected: Any, path: str = "result") -> int:
    """Compare structure and every leaf; return the number of validated leaves.

    Integers and text are exact. Nonzero floats use relative tolerance 1e-12
    with no blanket absolute tolerance (important for small p-values). Only
    dense-matrix marginal residuals use an absolute tolerance of 1e-12.
    """
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or actual.keys() != expected.keys():
            raise ValidationError(f"{path}: missing or unexpected fields")
        return sum(compare_records(actual[k], v, f"{path}.{k}") for k, v in expected.items())
    if isinstance(expected, (list, tuple)):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ValidationError(f"{path}: wrong list length or type")
        return sum(compare_records(a, e, f"{path}[{i}]") for i, (a, e) in enumerate(zip(actual, expected)))
    if isinstance(expected, float):
        if type(actual) not in (int, float) or not math.isfinite(actual):
            raise ValidationError(f"{path}: expected a finite number")
        residual = path.endswith(".local_marginal_max_error_from_maximally_mixed")
        if residual and not 0 <= actual <= 1e-12:
            raise ValidationError(f"{path}: invalid marginal residual")
        if not math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12 if residual else 0.0):
            raise ValidationError(f"{path}: {actual!r} != {expected!r}")
    elif type(actual) is not type(expected) or actual != expected:
        raise ValidationError(f"{path}: {actual!r} != {expected!r}")
    return 1


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValidationError(f"non-finite JSON constant: {value}")


def _load_csv(path: Path, expected: list[dict]) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or set(headers) != set(expected[0]):
            raise ValidationError(f"{path.name}: wrong or duplicate CSV columns")
        rows = list(reader)
    if len(rows) != len(expected):
        raise ValidationError(f"{path.name}: wrong row count")
    for row, reference in zip(rows, expected):
        if set(row) != set(reference):
            raise ValidationError(f"{path.name}: malformed CSV row")
        for key, target in reference.items():
            try:
                if isinstance(target, int):
                    row[key] = int(row[key])
                elif isinstance(target, float):
                    row[key] = float(row[key])
            except (TypeError, ValueError) as exc:
                raise ValidationError(f"{path.name}.{key}: invalid numeric cell") from exc
    return rows


def validate_results(results_dir: Path) -> int:
    """Validate every registered result file without changing them or the repository."""
    expected = _expected_results()
    actual_names = {p.name for p in results_dir.iterdir() if p.suffix in (".json", ".csv")}
    if actual_names != set(expected):
        raise ValidationError("missing or unexpected result files")
    leaves = 0
    for name, reference in expected.items():
        path = results_dir / name
        if path.is_symlink() or not path.is_file():
            raise ValidationError(f"{name}: expected a regular file")
        try:
            if path.suffix == ".csv":
                actual = _load_csv(path, reference)
            else:
                actual = json.loads(path.read_text(encoding="utf-8"),
                                    object_pairs_hook=_unique_object,
                                    parse_constant=_reject_constant)
            leaves += compare_records(actual, reference, name)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValidationError(f"{name}: cannot read valid result data") from exc
    return leaves
