#!/usr/bin/env python
# This script is based on the example at: https://raw.githubusercontent.com/nf-core/test-datasets/viralrecon/samplesheet/samplesheet_test_illumina_amplicon.csv

"""Provide a command line tool to validate and transform tabular samplesheets."""


import argparse
import csv
import logging
import sys
from collections import Counter
from pathlib import Path


logger = logging.getLogger()

<<<<<<< HEAD
    parser = argparse.ArgumentParser(description=Description, epilog=Epilog)
    parser.add_argument("FILE_IN", help="Input samplesheet file.")
    parser.add_argument("FILE_OUT", help="Output file.")
    parser.add_argument("INPUT_FORMAT", help="'FASTQ' or 'BAM' File Format.")
    return parser.parse_args(args)
=======
>>>>>>> TEMPLATE

class RowChecker:
    """
    Define a service that can validate and transform each given row.

    Attributes:
        modified (list): A list of dicts, where each dict corresponds to a previously
            validated and transformed row. The order of rows is maintained.

    """

    VALID_FORMATS = (
        ".fq.gz",
        ".fastq.gz",
    )

    def __init__(
        self,
        sample_col="sample",
        first_col="fastq_1",
        second_col="fastq_2",
        single_col="single_end",
        **kwargs,
    ):
        """
        Initialize the row checker with the expected column names.

        Args:
            sample_col (str): The name of the column that contains the sample name
                (default "sample").
            first_col (str): The name of the column that contains the first (or only)
                FASTQ file path (default "fastq_1").
            second_col (str): The name of the column that contains the second (if any)
                FASTQ file path (default "fastq_2").
            single_col (str): The name of the new column that will be inserted and
                records whether the sample contains single- or paired-end sequencing
                reads (default "single_end").

        """
        super().__init__(**kwargs)
        self._sample_col = sample_col
        self._first_col = first_col
        self._second_col = second_col
        self._single_col = single_col
        self._seen = set()
        self.modified = []

    def validate_and_transform(self, row):
        """
        Perform all validations on the given row and insert the read pairing status.

        Args:
            row (dict): A mapping from column headers (keys) to elements of that row
                (values).

        """
        self._validate_sample(row)
        self._validate_first(row)
        self._validate_second(row)
        self._validate_pair(row)
        self._seen.add((row[self._sample_col], row[self._first_col]))
        self.modified.append(row)

    def _validate_sample(self, row):
        """Assert that the sample name exists and convert spaces to underscores."""
        assert len(row[self._sample_col]) > 0, "Sample input is required."
        # Sanitize samples slightly.
        row[self._sample_col] = row[self._sample_col].replace(" ", "_")

    def _validate_first(self, row):
        """Assert that the first FASTQ entry is non-empty and has the right format."""
        assert len(row[self._first_col]) > 0, "At least the first FASTQ file is required."
        self._validate_fastq_format(row[self._first_col])

    def _validate_second(self, row):
        """Assert that the second FASTQ entry has the right format if it exists."""
        if len(row[self._second_col]) > 0:
            self._validate_fastq_format(row[self._second_col])

    def _validate_pair(self, row):
        """Assert that read pairs have the same file extension. Report pair status."""
        if row[self._first_col] and row[self._second_col]:
            row[self._single_col] = False
            assert (
                Path(row[self._first_col]).suffixes == Path(row[self._second_col]).suffixes
            ), "FASTQ pairs must have the same file extensions."
        else:
            row[self._single_col] = True

    def _validate_fastq_format(self, filename):
        """Assert that a given filename has one of the expected FASTQ extensions."""
        assert any(filename.endswith(extension) for extension in self.VALID_FORMATS), (
            f"The FASTQ file has an unrecognized extension: {filename}\n"
            f"It should be one of: {', '.join(self.VALID_FORMATS)}"
        )

    def validate_unique_samples(self):
        """
        Assert that the combination of sample name and FASTQ filename is unique.

        In addition to the validation, also rename the sample if more than one sample,
        FASTQ file combination exists.

        """
        assert len(self._seen) == len(self.modified), "The pair of sample name and FASTQ must be unique."
        if len({pair[0] for pair in self._seen}) < len(self._seen):
            counts = Counter(pair[0] for pair in self._seen)
            seen = Counter()
            for row in self.modified:
                sample = row[self._sample_col]
                seen[sample] += 1
                if counts[sample] > 1:
                    row[self._sample_col] = f"{sample}_T{seen[sample]}"


def sniff_format(handle):
    """
    Detect the tabular format.

    Args:
        handle (text file): A handle to a `text file`_ object. The read position is
        expected to be at the beginning (index 0).

    Returns:
        csv.Dialect: The detected tabular format.

    .. _text file:
        https://docs.python.org/3/glossary.html#term-text-file

def check_samplesheet(file_in, file_out, input_format):
    """
    peek = handle.read(2048)
    sniffer = csv.Sniffer()
    if not sniffer.has_header(peek):
        logger.critical(f"The given sample sheet does not appear to contain a header.")
        sys.exit(1)
    dialect = sniffer.sniff(peek)
    handle.seek(0)
    return dialect


    sample,bam_file
    SAMPLE_PE,SAMPLE_PE_RUN1.bam
    SAMPLE_PE,SAMPLE_PE_RUN2.bam

    For an example see:
    https://raw.githubusercontent.com/nf-core/test-datasets/viralrecon/samplesheet/samplesheet_test_illumina_amplicon.csv
    """
    Check that the tabular samplesheet has the structure expected by nf-core pipelines.

    Validate the general shape of the table, expected columns, and each row. Also add
    an additional column which records whether one or two FASTQ reads were found.

        if ( input_format == "FASTQ" ):
            ## Check header
            MIN_COLS = 2
            HEADER = ["sample", "fastq_1", "fastq_2"]
            header = [x.strip('"') for x in fin.readline().strip().split(",")]
            if header[: len(HEADER)] != HEADER:
                print("ERROR: Please check samplesheet header -> {} != {}".format(",".join(header), ",".join(HEADER)))
                sys.exit(1)

            ## Check sample entries
            for line in fin:
                lspl = [x.strip().strip('"') for x in line.strip().split(",")]

                # Check valid number of columns per row
                if len(lspl) < len(HEADER):
                    print_error(
                        "Invalid number of columns (minimum = {})!".format(len(HEADER)),
                        "Line",
                        line,
                    )
                num_cols = len([x for x in lspl if x])
                if num_cols < MIN_COLS:
                    print_error(
                        "Invalid number of populated columns (minimum = {})!".format(MIN_COLS),
                        "Line",
                        line,
                    )

                ## Check sample name entries
                sample, fastq_1, fastq_2 = lspl[: len(HEADER)]
                sample = sample.replace(" ", "_")
                if not sample:
                    print_error("Sample entry has not been specified!", "Line", line)

                ## Check FastQ file extension
                for fastq in [fastq_1, fastq_2]:
                    if fastq:
                        if fastq.find(" ") != -1:
                            print_error("FastQ file contains spaces!", "Line", line)
                        if not fastq.endswith(".fastq.gz") and not fastq.endswith(".fq.gz"):
                            print_error(
                                "FastQ file does not have extension '.fastq.gz' or '.fq.gz'!",
                                "Line",
                                line,
                            )
                ## Auto-detect paired-end/single-end
                sample_info = []  ## [single_end, fastq_1, fastq_2]
                if sample and fastq_1 and fastq_2:  ## Paired-end short reads
                    sample_info = ["0", fastq_1, fastq_2]
                elif sample and fastq_1 and not fastq_2:  ## Single-end short reads
                    sample_info = ["1", fastq_1, fastq_2]
                else:
                    print_error("Invalid combination of columns provided!", "Line", line)

                ## Create sample mapping dictionary = { sample: [ single_end, fastq_1, fastq_2 ] }
                if sample not in sample_mapping_dict:
                    sample_mapping_dict[sample] = [sample_info]
                else:
                    if sample_info in sample_mapping_dict[sample]:
                        print_error("Samplesheet contains duplicate rows!", "Line", line)
                    else:
                        sample_mapping_dict[sample].append(sample_info)

        elif input_format == "BAM":
            MIN_COLS = 2
            HEADER = ["sample", "bam"]
            header = [x.strip('"') for x in fin.readline().strip().split(",")]
            if header[: len(HEADER)] != HEADER:
                print("ERROR: Please check samplesheet header -> {} != {}".format(",".join(header), ",".join(HEADER)))
                sys.exit(1)

            ## Check sample entries
            for line in fin:
                lspl = [x.strip().strip('"') for x in line.strip().split(",")]

                # Check valid number of columns per row
                if len(lspl) < len(HEADER):
                    print_error(
                        "Invalid number of columns (minimum = {})!".format(len(HEADER)),
                        "Line",
                        line,
                    )
                num_cols = len([x for x in lspl if x])
                if num_cols < MIN_COLS:
                    print_error(
                        "Invalid number of populated columns (minimum = {})!".format(MIN_COLS),
                        "Line",
                        line,
                    )

                ## Check sample name entries
                sample, bam = lspl[: len(HEADER)]
                sample = sample.replace(" ", "_")
                if not sample:
                    print_error("Sample entry has not been specified!", "Line", line)

                ## Check bam file extension
                if bam:
                    if bam.find(" ") != -1:
                        print_error("BAM file contains spaces!", "Line", line)
                    if not bam.endswith(".bam"):
                        print_error(
                            "Bam file does not have extension '.bam'!",
                            "Line",
                            line,
                        )
                sample_info = ["1", bam]

                ## Create sample mapping dictionary = { sample: [ bam ] }
                if sample not in sample_mapping_dict:
                    sample_mapping_dict[sample] = [sample_info]
                else:
                    if sample_info in sample_mapping_dict[sample]:
                        print_error("Samplesheet contains duplicate rows!", "Line", line)
                    else:
                        sample_mapping_dict[sample].append(sample_info)

        else:
            print_error("INPUT_FORMAT needs to be either 'FASTQ' or 'BAM'")
            sys.exit(1)

        ## Write validated samplesheet with appropriate columns
        if len(sample_mapping_dict) > 0:
            out_dir = os.path.dirname(file_out)
            make_dir(out_dir)
            with open(file_out, "w") as fout:
                if input_format == "FASTQ":
                    fout.write(",".join(["sample", "single_end", "fastq_1", "fastq_2"]) + "\n")
                    for sample in sorted(sample_mapping_dict.keys()):

                        ## Check that multiple runs of the same sample are of the same datatype
                        if not all(x[0] == sample_mapping_dict[sample][0][0] for x in sample_mapping_dict[sample]):
                            print_error("Multiple runs of a sample must be of the same datatype!", "Sample: {}".format(sample))

                        for idx, val in enumerate(sample_mapping_dict[sample]):
                            fout.write(",".join(["{}_T{}".format(sample, idx + 1)] + val) + "\n")
                elif input_format == "BAM":
                    fout.write(",".join(["sample", "idx", "bam"]) + "\n")
                    for sample in sorted(sample_mapping_dict.keys()):

                        for idx, val in enumerate(sample_mapping_dict[sample]):
                            fout.write(",".join(["{}".format(sample)] + val) + "\n")

        else:
            print_error("No entries to process!", "Samplesheet: {}".format(file_in))




def main(args=None):
    args = parse_args(args)
    check_samplesheet(args.FILE_IN, args.FILE_OUT, args.INPUT_FORMAT)


if __name__ == "__main__":
    sys.exit(main())
