# Barcode Crossover Analysis

This project demonstrates a reproducible bioinformatics workflow for quantifying barcode crossover in Oxford Nanopore sequencing data. Using Nextflow, Python, samtools, and minimap2, the workflow compares sequencing runs before and after a protocol change to estimate whether non-target sequence carryover was reduced.

## Objective

Determine whether a protocol modification reduced the amount of non-D5405 sequence detected within reads assigned to the D5405 barcode.

## Findings

Estimated barcode crossover decreased from **0.0878%** before the protocol change to **0.0141%** afterward.

The analysis indicates that low-level barcode crossover was present in the original run and that the protocol modification reduced estimated crossover by approximately **six-fold**.

## Workflow

The analysis begins with two unaligned Oxford Nanopore BAM files representing sequencing runs before and after the protocol change.

The workflow performs the following steps:

1. Convert unaligned BAM files to FASTQ using samtools.
2. Align reads to a combined reference using minimap2.
3. Count primary alignments for each reference sequence.
4. Calculate estimated barcode crossover by treating non-D5405 alignments as crossover events.
5. Generate a summary table and visualization comparing both runs.

The combined reference contains:

- D5405
- *Homo sapiens*
- *Oryza sativa*
- Lambda phage

## Results

| Run | D5405 | Human | Rice | Lambda | Non-D5405 | Estimated Crossover |
|------|-------:|------:|-----:|--------:|----------:|--------------------:|
| Before | 93,334 | 17 | 29 | 36 | 82 | 0.0878% |
| After | 99,630 | 5 | 4 | 5 | 14 | 0.0141% |

## Biological Interpretation

Nearly all reads assigned to the D5405 barcode aligned back to the expected reference in both sequencing runs.

The original dataset contained a small number of reads aligning to human, rice, and lambda references, consistent with low-level barcode crossover. Following the protocol modification, non-D5405 alignments decreased across all reference genomes, suggesting the protocol successfully reduced crossover.

These findings suggest that low-level barcode crossover was present in the original sequencing run and that the protocol modification substantially reduced it.

## Running the Workflow

```bash
nextflow run workflow/main.nf
```

Primary outputs are written to:

```
results/nextflow/
```

Key output files:

- `results/nextflow/crossover_summary.tsv`
- `plots/crossover_percent_before_after.png`

## Repository Structure

```
.
├── data/
│   ├── references/
│   └── unaligned_bams/
├── workflow/
│   └── main.nf
├── scripts/
│   ├── summarize_crossover.py
│   └── plot_crossover.py
├── results/
│   └── nextflow/
│       └── crossover_summary.tsv
├── plots/
│   └── crossover_percent_before_after.png
├── nextflow.config
├── .gitignore
└── README.md
```

Large sequencing datasets, reference genomes, and intermediate workflow files are excluded from version control.

## Input Files

Reference FASTA files should be placed in:

```
data/references/
```

Input BAM files should be placed in:

```
data/unaligned_bams/
```

Example input files:

- `bc_zymo_3a_26-124-0051.subsampled_100000.bam`
- `bc_zymo_1b_26-124-0070.subsampled_100000.bam`

## Software

- Nextflow
- samtools
- minimap2
- Python 3
- matplotlib

## Skills Demonstrated

- Nextflow workflow development
- Oxford Nanopore sequencing analysis
- Sequence alignment with minimap2
- BAM/FASTQ processing with samtools
- Python workflow automation
- Data summarization and visualization
- Reproducible bioinformatics pipelines

## Notes

Development and testing were performed in GitHub Codespaces. During development, subset reference genomes were used because indexing the full human genome exceeded available Codespaces resources.

The workflow is designed so the same analysis can be performed with full reference genomes in an environment with sufficient computational resources.

## Future Improvements

- Support parameterized reference inputs through Nextflow configuration.
- Generate plots directly within the Nextflow workflow.
- Add additional alignment quality metrics to the summary report.
- Containerize the workflow for fully portable execution.

## Author

**Shiloh Cadere**

Bioinformatics professional specializing in NGS workflows, reproducible pipeline development, data validation, and laboratory data systems.
