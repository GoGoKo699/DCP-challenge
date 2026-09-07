"""Mutation tests: correct data must pass and corrupted data must fail."""
import copy
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from dcp_challenge.result_validation import ValidationError, validate_results

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def records(tmp_path):
    destination = tmp_path / "results"
    shutil.copytree(ROOT / "results", destination)
    return destination


def _leaves(value, prefix=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _leaves(child, prefix+(key,))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from _leaves(child, prefix+(i,))
    else:
        yield prefix, value


def _alter(value):
    if isinstance(value, int):
        return value + max(1, abs(value)//10)
    if isinstance(value, float):
        return value + max(0.125, abs(value)*0.1)
    return value + " [deliberate corruption]"


def test_real_records_pass(records):
    assert validate_results(records) == 1268


def test_every_json_leaf_is_checked(records):
    mutations = 0
    for path in sorted(records.glob("*.json")):
        original = path.read_text()
        data = json.loads(original)
        for keys, value in _leaves(data):
            corrupted = copy.deepcopy(data)
            target = corrupted
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = _alter(value)
            path.write_text(json.dumps(corrupted))
            with pytest.raises(ValidationError):
                validate_results(records)
            mutations += 1
            path.write_text(original)
    assert mutations == 1220


def test_every_csv_cell_is_checked(records):
    path = records / "figure5_corrected.csv"
    original = path.read_text()
    reader = csv.DictReader(original.splitlines())
    rows, headers = list(reader), reader.fieldnames
    for i, row in enumerate(rows):
        for key in row:
            corrupted = copy.deepcopy(rows)
            corrupted[i][key] = "999999" if row[key] != "999999" else "0"
            with path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=headers)
                writer.writeheader()
                writer.writerows(corrupted)
            with pytest.raises(ValidationError):
                validate_results(records)
            path.write_text(original)


def test_corrupting_duplicate_records_together_still_fails(records):
    for name in ("heralded_witness_results.json", "correction_core_results.json"):
        path = records / name
        data = json.loads(path.read_text())
        witness = data if name.startswith("heralded") else data["heralded_witness"]
        witness["N2"]["separable_confidence_upper_bound"] = 0.99
        path.write_text(json.dumps(data))
    with pytest.raises(ValidationError, match="confidence"):
        validate_results(records)


@pytest.mark.parametrize("damage", ["missing_file", "extra_file", "missing_key", "extra_key",
    "empty_rows", "duplicate_key", "nan", "infinity", "bool_as_count", "extra_csv_row"])
def test_schema_and_nonfinite_corruption(records, damage):
    path = records / "one_sample_optimality.json"
    data = json.loads(path.read_text())
    if damage == "missing_file":
        path.unlink()
    elif damage == "extra_file":
        (records / "unreviewed.json").write_text("{}")
    elif damage == "missing_key":
        del data[0]["n"]
    elif damage == "extra_key":
        data[0]["unreviewed"] = 1
    elif damage == "empty_rows":
        data = []
    elif damage == "duplicate_key":
        path.write_text('[{"n":1,"n":2}]')
    elif damage == "nan":
        data[0]["optimal_all_H_success"]["decimal"] = float("nan")
    elif damage == "infinity":
        data[0]["optimal_all_H_success"]["decimal"] = float("inf")
    elif damage == "bool_as_count":
        data[0]["n"] = True
    elif damage == "extra_csv_row":
        csv_path = records / "figure5_corrected.csv"
        csv_path.write_text(csv_path.read_text()+csv_path.read_text().splitlines()[1]+"\n")
    if damage not in ("missing_file", "duplicate_key"):
        path.write_text(json.dumps(data))
    with pytest.raises(ValidationError):
        validate_results(records)


def test_small_p_value_cannot_be_rounded_to_zero(records):
    path = records / "heralded_witness_results.json"
    data = json.loads(path.read_text())
    data["finite_sample_examples"]["at_most_20_errors_among_200"] = 0
    path.write_text(json.dumps(data))
    with pytest.raises(ValidationError):
        validate_results(records)


def test_matrix_residual_tolerance_is_not_a_probability_tolerance(records):
    path = records / "heralded_witness_results.json"
    data = json.loads(path.read_text())
    data["dense_full_state_N2"]["local_marginal_max_error_from_maximally_mixed"] = 1e-13
    path.write_text(json.dumps(data))
    validate_results(records)
    data["N2"]["honest_wrong_conclusive"] = 1e-13
    path.write_text(json.dumps(data))
    with pytest.raises(ValidationError):
        validate_results(records)


def test_validation_remains_enabled_under_python_optimization(records):
    (records / "one_sample_optimality.json").write_text("[]")
    result = subprocess.run([sys.executable, "-O", str(ROOT / "scripts/validate_committed_results.py"),
                             "--results-dir", str(records)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "ValidationError" in result.stderr
