#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot estimated barcode crossover before and after protocol tweak."
    )
    parser.add_argument(
        "--input",
        default="results/nextflow/crossover_summary.tsv",
        help="Path to crossover summary TSV.",
    )
    parser.add_argument(
        "--out",
        default="plots/crossover_percent_before_after.png",
        help="Output plot path.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.out)

    runs = []
    percentages = []

    with input_path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            runs.append(row["run"])
            percentages.append(float(row["crossover_percent"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(5, 4))
    plt.bar(runs, percentages)
    plt.ylabel("Estimated crossover (%)")
    plt.xlabel("Run")
    plt.title("Estimated barcode crossover before vs after protocol tweak")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()