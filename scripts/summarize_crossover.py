#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv


REFERENCE_MAP = {
    "D5405": "D5405",
    "chr1": "human",
    "NC_089035.1": "rice",
    "lambda": "lambda",
}


def read_counts(path: Path) -> dict[str, int]:
    counts = {"D5405": 0, "human": 0, "rice": 0, "lambda": 0}

    with path.open() as handle:
        for line in handle:
            if not line.strip():
                continue

            ref, count = line.strip().split()
            species = REFERENCE_MAP.get(ref, ref)
            counts[species] = counts.get(species, 0) + int(count)

    return counts


def summarize(run_name: str, path: Path) -> dict[str, str | int | float]:
    counts = read_counts(path)

    total_primary_mapped = sum(counts.values())
    non_d5405 = total_primary_mapped - counts["D5405"]
    crossover_percent = (non_d5405 / total_primary_mapped) * 100 if total_primary_mapped else 0

    return {
        "run": run_name,
        "total_primary_mapped": total_primary_mapped,
        "D5405": counts["D5405"],
        "human": counts["human"],
        "rice": counts["rice"],
        "lambda": counts["lambda"],
        "non_D5405": non_d5405,
        "crossover_percent": round(crossover_percent, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize estimated barcode crossover from reference-count TSV files."
    )
    parser.add_argument("--before", default="results/before.reference_counts.tsv")
    parser.add_argument("--after", default="results/after.reference_counts.tsv")
    parser.add_argument("--out", default="results/crossover_summary.tsv")

    args = parser.parse_args()

    inputs = {
        "before": Path(args.before),
        "after": Path(args.after),
    }

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = [summarize(run_name, path) for run_name, path in inputs.items()]

    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "run",
                "total_primary_mapped",
                "D5405",
                "human",
                "rice",
                "lambda",
                "non_D5405",
                "crossover_percent",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output}")


if __name__ == "__main__":
    main()