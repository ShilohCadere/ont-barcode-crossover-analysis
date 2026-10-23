import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("summary", ROOT / "scripts" / "summarize_crossover.py")
summary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(summary)

class CrossoverSummaryTests(unittest.TestCase):
    def test_reference_count_mapping_and_percent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "counts.tsv"
            path.write_text("D5405 98\nchr1 1\nNC_089035.1 1\n")
            result = summary.summarize("demo", path)
            self.assertEqual(result["total_primary_mapped"], 100)
            self.assertEqual(result["non_D5405"], 2)
            self.assertEqual(result["crossover_percent"], 2.0)

    def test_saved_results_arithmetic(self):
        path = ROOT / "results" / "nextflow" / "crossover_summary.tsv"
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual([r["run"] for r in rows], ["before", "after"])
        expected = {"before": (93416, 82), "after": (99644, 14)}
        for row in rows:
            total, unexpected = expected[row["run"]]
            self.assertEqual(int(row["total_primary_mapped"]), total)
            self.assertEqual(int(row["non_D5405"]), unexpected)
            self.assertEqual(sum(int(row[k]) for k in ("D5405", "human", "rice", "lambda")), total)
            self.assertEqual(round(100 * unexpected / total, 4), float(row["crossover_percent"]))

if __name__ == "__main__":
    unittest.main()
