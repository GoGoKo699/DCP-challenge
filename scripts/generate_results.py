"""Regenerate reference outputs; large Monte Carlo runs are opt-in."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from dcp_challenge.reference_results import build_results

ROOT = Path(__file__).resolve().parents[1]


def main(run_large_monte_carlo: bool = False, output: Path | None = None) -> None:
    destination = output if output is not None else ROOT / "results"
    destination.mkdir(parents=True, exist_ok=True)
    records = build_results(run_large_monte_carlo)
    for name, data in records.items():
        path = destination / name
        if path.suffix == ".csv":
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=sorted(data[0]))
                writer.writeheader()
                writer.writerows(data)
        else:
            path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n",
                            encoding="utf-8")
    print(f"Wrote {len(records)} result files to {destination}.")
    if not run_large_monte_carlo:
        print("Monte Carlo counts are archived records, not newly simulated in this mode.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="separate directory for regenerated files")
    parser.add_argument("--monte-carlo", action="store_true", help="rerun the large Figure 5 simulations")
    args = parser.parse_args()
    main(args.monte_carlo, args.output)
