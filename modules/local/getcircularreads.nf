process GETCIRCULARREADS {
    tag "$meta.id"
    label 'process_low'

    //Test adding a containerhere
    conda (params.enable_conda ? 'bioconda::unicycler=0.5.0=py39h2add14b_1' : null)
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/unicycler:0.5.0--py39h2add14b_1' :
        'quay.io/biocontainers/unicycler:0.5.0--py37h09c1ff4_1' }"

    input:
    tuple val(meta), path(fastq)

    output:
    tuple val(meta), path("*unicycler.circular.fastq.gz"), optional: true, emit: fastq

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"

    """
    zcat $fastq > temp.fastq
    if grep -q "circular=true" temp.fastq; then
        cat temp.fastq | grep -A3 "circular=true" | \\
            grep -v "^--" | \\
            gzip --no-name > \\
            ${prefix}.unicycler.circular.fastq.gz
    fi
    rm temp.fastq
    """
}
