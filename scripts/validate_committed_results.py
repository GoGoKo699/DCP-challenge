"""Validate every committed scientific result field, without modifying files."""
from __future__ import annotations

import argparse
from pathlib import Path

from dcp_challenge.result_validation import validate_results

ROOT = Path(__file__).resolve().parents[1]


def main(results_dir: Path = ROOT / "results") -> None:
    leaves = validate_results(results_dir)
    print(f"Committed result validation passed: {leaves} fields.")
    print("Exact values recomputed; floating diagnostics checked with declared tolerances.")
    print("Monte Carlo records: archived counts/metadata and Wilson intervals checked; not re-simulated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results")
    main(parser.parse_args().results_dir)
