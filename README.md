# Barcode Crossover Analysis

I built this workflow to investigate possible barcode crossover in Oxford Nanopore sequencing data. The analysis compares reads assigned to a D5405 barcode before and after a protocol change intended to reduce crossover.

The goal was to answer a practical question: did the protocol change reduce the amount of non-D5405 sequence showing up in the D5405 barcode?

## Approach

The input files were unaligned BAM files from two D5405 barcode runs:

- before protocol change
- after protocol change

The workflow:

1. Converts each BAM file to FASTQ
2. Aligns reads to a combined reference with minimap2
3. Counts primary alignments by reference
4. Treats non-D5405 alignments as estimated barcode crossover
5. Compares crossover before and after the protocol change

The combined reference contains:

- D5405
- Homo sapiens
- Oryza sativa
- Lambda phage

## Results

| Run | D5405 reads | Human | Rice | Lambda | Non-D5405 reads | Estimated crossover |
|---|---:|---:|---:|---:|---:|---:|
| Before protocol change | 93,334 | 17 | 29 | 36 | 82 | 0.0878% |
| After protocol change | 99,630 | 5 | 4 | 5 | 14 | 0.0141% |

Based on this analysis, the protocol change appears to have reduced estimated barcode crossover from 0.0878% to 0.0141%, or about a 6-fold reduction.

## Interpretation

Most reads assigned to the D5405 barcode aligned back to D5405 in both runs. The original run had a small but detectable number of reads aligning to the other multiplexed references. After the protocol change, those non-D5405 alignments dropped across human, rice, and lambda.

This supports Felix's concern that low-level crossover was present in the original run and suggests the protocol change reduced it substantially.

## Workflow

The reproducible workflow is implemented in Nextflow:

```bash
nextflow run workflow/main.nf
```

The workflow writes outputs to:

```text
results/nextflow/
```

Key output files:

```text
results/nextflow/crossover_summary.tsv
plots/crossover_percent_before_after.png
```

## Repository Structure

```text
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

Large sequencing and reference files are excluded from version control.

## Inputs

Place reference FASTA files here:

```text
data/references/
```

Place unaligned BAM files here:

```text
data/unaligned_bams/
```

Expected BAM files:

```text
bc_zymo_3a_26-124-0051.subsampled_100000.bam
bc_zymo_1b_26-124-0070.subsampled_100000.bam
```

## Software

This workflow uses:

- Nextflow
- samtools
- minimap2
- Python 3
- matplotlib

## Notes

Development and testing were performed in GitHub Codespaces. During testing, subset references were used because indexing the full human reference exceeded available Codespaces resources.

The workflow is written so the same analysis can be run with full references in an environment with sufficient memory.

## Author
### Shiloh Cadere
