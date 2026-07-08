# Barcode Crossover Analysis

## At a Glance

- Reproducible Nextflow workflow quantifying barcode crossover in Oxford Nanopore sequencing data.
- Processes unaligned BAM files through FASTQ conversion, sequence alignment, and reference quantification.
- Compares sequencing runs before and after protocol optimization to estimate barcode crossover.
- Demonstrates workflow development, sequencing analysis, and biological interpretation using simulated demonstration datasets.

---

## Overview

Barcode Crossover Analysis is a portfolio project that models a reproducible sequencing analysis workflow for estimating barcode crossover in Oxford Nanopore sequencing data. Beginning with unaligned BAM files, the workflow converts reads to FASTQ, aligns sequences against a combined reference genome, quantifies primary alignments, and estimates barcode crossover before and after a protocol modification.

The repository emphasizes workflow automation, reproducible sequencing analysis, and biological interpretation while using demonstration datasets and openly available bioinformatics software.

---

## Why This Project Exists

Sequencing workflows often require more than generating alignments. Analytical workflows must transform raw sequencing data into interpretable biological conclusions.

This project demonstrates that process.

Using Nextflow, samtools, minimap2, and Python, the workflow estimates barcode crossover by comparing expected and unexpected reference alignments before and after a laboratory protocol modification.

The focus is not protocol optimization itself. Instead, the project demonstrates reproducible workflow development, sequencing analysis, and quantitative biological interpretation.

---

## Workflow Architecture

Barcode Crossover Analysis models a sequencing analysis workflow beginning with unaligned Oxford Nanopore sequencing data. Each analytical stage performs one responsibility while maintaining separation between workflow execution, summarization, and visualization.

```
Unaligned BAM Files
        │
        ▼
FASTQ Conversion
(samtools)
        │
        ▼
Sequence Alignment
(minimap2)
        │
        ▼
Reference Quantification
        │
        ▼
Barcode Crossover Estimation
        │
        ▼
Summary Tables
        └── Visualization
```

---

## Repository Structure

```
barcode-crossover-analysis/
├── workflow/          # Nextflow workflow definition
├── scripts/           # Analysis and visualization scripts
├── data/              # Example input datasets
├── results/           # Generated summary outputs
├── plots/             # Generated visualizations
├── nextflow.config
└── README.md
```

The repository separates workflow execution, analytical summarization, and visualization into independent components, allowing each stage of the analysis to evolve while keeping responsibilities clearly defined.

---

## Current Capabilities

Current functionality includes:

- Loading unaligned Oxford Nanopore BAM files.
- Converting BAM files to FASTQ using samtools.
- Aligning sequencing reads using minimap2.
- Quantifying primary alignments across multiple reference genomes.
- Estimating barcode crossover from non-target alignments.
- Comparing sequencing runs before and after protocol modification.
- Generating summary tables and comparative visualizations.
- Executing reproducibly through Nextflow.

---

## Example Inputs

Example datasets are included to demonstrate the complete analysis workflow.

### Sequencing Data

- Unaligned Oxford Nanopore BAM files

### Combined Reference

- D5405
- Homo sapiens
- Oryza sativa
- Lambda phage

The included datasets are demonstration subsets intended to illustrate workflow behavior rather than represent complete sequencing experiments.

---

## Execution

Run the workflow:

```bash
nextflow run workflow/main.nf
```

---

## Example Outputs

Successful execution generates analytical outputs summarizing barcode crossover.

### Summary Table

Reports reference alignment counts and estimated barcode crossover for each sequencing run.

### Comparative Visualization

Displays estimated crossover before and after protocol optimization.

The generated outputs demonstrate quantitative sequencing analysis rather than clinical interpretation.

---

## Results

| Run | Estimated Barcode Crossover |
|------|----------------------------:|
| Before | 0.0878% |
| After | 0.0141% |

The protocol modification reduced estimated barcode crossover by approximately six-fold while maintaining expected alignment to the target barcode.

---

## Design Decisions

Several architectural decisions intentionally shape this project.

### Workflow Automation

Nextflow coordinates each analytical stage while maintaining reproducible execution.

### Separation of Responsibilities

Workflow execution, analytical summarization, and visualization are implemented independently to improve readability and maintainability.

### Combined Reference Alignment

Reads are aligned against a combined reference genome so unexpected alignments can be quantified directly as potential barcode crossover.

### Biological Interpretation

Analytical outputs are translated into measurable biological conclusions while preserving separation between computation and interpretation.

---

## Testing

This project emphasizes deterministic workflow execution through reproducible sequencing analysis.

Identical sequencing inputs produce consistent alignment summaries, barcode crossover estimates, and visualizations across repeated executions.

---

## Future Improvements

Planned future development includes:

- Supporting parameterized reference inputs through Nextflow configuration.
- Integrating visualization directly into the workflow.
- Expanding alignment quality metrics.
- Containerizing the workflow for fully reproducible execution.

Future development will continue to prioritize reproducible workflow design, maintainable software architecture, and quantitative sequencing analysis.

---

## Technologies Used

Nextflow • Python • samtools • minimap2 • matplotlib

---

## Author

**Shiloh Cadere**

Bioinformatics analyst focused on genomics QC, analytical review, workflow development, and reproducible bioinformatics software.
