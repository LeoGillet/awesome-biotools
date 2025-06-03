#!/usr/bin/env python3
"""
Renames typical Illumina iSeq 100 output alignment files to
easily readable and scriptable file names.
<SampleName>_S<SampleNumber>_L001_R<ReadNumber>_001.fastq.gz
    becomes
<SampleName>_R<ReadNumber>.fastq.gz
"""
import argparse
import os


def rename_all_files(input_dir, file_paths):
    """
    Renames files from list of fastq.gz files found in input directory.
    """
    for fp in file_paths:
        if fp.count('_') == 4:
            # sampleName_index_line_read_line.fastq.gz
            *sample_name, _, _, read, _ = fp.split('_')
            new_filename = f"{sample_name}_{read}.fastq.gz"
            os.rename(os.path.join(input_dir, fp),
                      os.path.join(input_dir, new_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="fastq_filename_cleaner.py")
    parser.add_argument("input_dir", default=".")

    args = parser.parse_args()
    if not os.path.isdir(args.input_dir):
        raise NotADirectoryError(
            f"Input argument does not point to a valid directory. input_dir:{args.input_dir}")

    files_in_directory = os.listdir(args.input_dir)
    if not files_in_directory:
        raise FileNotFoundError(
            f"Input directory is empty or permissions are insufficient. input_dir:{args.input_dir}")

    fastq_files_in_directory = [
        fp for fp in files_in_directory if fp.endswith('.fastq.gz')]
    if not fastq_files_in_directory:
        raise FileNotFoundError(
            f"No files with '.fastq.gz' extension found in directory. input_dir:{args.input_dir}")

    rename_all_files(args.input_dir, fastq_files_in_directory)
