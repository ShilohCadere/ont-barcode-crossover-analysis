nextflow.enable.dsl = 2

params.before_bam = "data/unaligned_bams/bc_zymo_3a_26-124-0051.subsampled_100000.bam"
params.after_bam  = "data/unaligned_bams/bc_zymo_1b_26-124-0070.subsampled_100000.bam"

params.reference_fasta = "data/references/subset/combined_reference_subset.fa"
params.outdir = "results/nextflow"


process BUILD_MINIMAP2_INDEX {
    tag "combined_reference"

    publishDir "${params.outdir}/reference", mode: "copy"

    input:
    path reference_fasta

    output:
    path "combined_reference.mmi"

    script:
    """
    minimap2 -d combined_reference.mmi ${reference_fasta}
    """
}


process BAM_TO_FASTQ {
    tag "${sample}"

    publishDir "${params.outdir}/fastq", mode: "copy"

    input:
    tuple val(sample), path(bam)

    output:
    tuple val(sample), path("${sample}.fastq")

    script:
    """
    samtools fastq ${bam} > ${sample}.fastq
    """
}


process ALIGN_READS {
    tag "${sample}"

    publishDir "${params.outdir}/alignments", mode: "copy"

    input:
    tuple val(sample), path(fastq), path(index)

    output:
    tuple val(sample), path("${sample}.aligned.sorted.bam")

    script:
    """
    minimap2 -ax map-ont ${index} ${fastq} \
      | samtools sort -o ${sample}.aligned.sorted.bam
    """
}


process COUNT_REFERENCES {
    tag "${sample}"

    publishDir "${params.outdir}/counts", mode: "copy"

    input:
    tuple val(sample), path(bam)

    output:
    tuple val(sample), path("${sample}.reference_counts.tsv")

    script:
    """
    samtools view -F 2308 ${bam} \
      | awk '{count[\$3]++} END {for (ref in count) print ref, count[ref]}' \
      | sort > ${sample}.reference_counts.tsv
    """
}


process SUMMARIZE_CROSSOVER {
    tag "crossover_summary"

    publishDir "${params.outdir}", mode: "copy"

    input:
    path before_counts
    path after_counts
    path summary_script

    output:
    path "crossover_summary.tsv"

    script:
    """
    python3 ${summary_script} \
      --before ${before_counts} \
      --after ${after_counts} \
      --out crossover_summary.tsv
    """
}


workflow {
    reference_ch = Channel.fromPath(params.reference_fasta, checkIfExists: true)

    bam_ch = Channel.of(
        ["before", file(params.before_bam)],
        ["after", file(params.after_bam)]
    )

    index_ch = BUILD_MINIMAP2_INDEX(reference_ch)

    fastq_ch = BAM_TO_FASTQ(bam_ch)

    fastq_with_index_ch = fastq_ch.combine(index_ch)

    aligned_ch = ALIGN_READS(fastq_with_index_ch)

    counts_ch = COUNT_REFERENCES(aligned_ch)

    before_counts_ch = counts_ch
        .filter { sample, counts -> sample == "before" }
        .map { sample, counts -> counts }

    after_counts_ch = counts_ch
        .filter { sample, counts -> sample == "after" }
        .map { sample, counts -> counts }

    summary_script_ch = Channel.fromPath("scripts/summarize_crossover.py", checkIfExists: true)

    SUMMARIZE_CROSSOVER(before_counts_ch, after_counts_ch, summary_script_ch)
}