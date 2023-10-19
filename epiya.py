#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple cagA EPIYA motif finder
Accepts both single sequence from launch arguments and FASTA files
Returns a string of all motifs found for each sequence

Usage: epiya.py [-h] (-s SEQ | -f FILE) [--sep SEP] [-nr]
options:
    -h, --help            show this help message and exit
    -s SEQ, --seq SEQ     Single cagA sequence as argument
    -f FILE, --file FILE  FASTA file containing one or more cagA sequences
    --sep SEP             Separator for result output. Using ',' is great for CSV files
    -nr, --norareseg      Make rare patterns such as B', B'', B''' appear as B


citing:     Xue, Zhijing et al.
            Diversity of 3' variable region of cagA gene in Helicobacter pylori strains 
                isolated from Chinese population.
            13 Apr. 2021
            doi:10.1186/s13099-021-00419-3
            
author:     Léo Gillet <leo@leogillet.com> (CHU de Bordeaux)
date:       october 2023
"""
import argparse

from Bio import SeqIO


def search_motif(caga_seq, norareseg=False) -> str:
    """Scans string for any EPIYA motif, returns found genotype.

    Args:
        caga_seq (str): cagA sequence
        norareseg (bool, optional): If True, rare segment codes (', '', ''') will be ignored from output. Defaults to False.

    Returns:
        str: genotype of sequence
    """
    epiya_motifs = {
        "": [
            "EPIYA",
        ],
        "'": [
            "EPIYT",
        ],
        "''": [
            "ESIYA",
        ],
        "'''": [
            "ESIYT",
        ],
        "*": ["EPVYA", "EPLYA", "ELIYA", "EHIYA", "EAIYA", "APIYA", "ELIYA", "DPIYA"],
    }

    all_motifs = []
    for motif_list in epiya_motifs.values():
        all_motifs.extend(motif_list)

    epiya_4aa = {
        "A": [
            "QVNK",
            "KVNK",
            "EVNK",
        ],
        "B": [
            "QVAK",
        ],
        "C": [
            "TIDD",
            "TIDE",
            "TIED",
        ],
        "D": [
            "TIDF",
        ],
    }

    found_motifs = []

    for i in range(len(caga_seq) - 9):
        if caga_seq[i : i + 5] in all_motifs:
            this_seg = ""
            if not norareseg:
                for seg, motifs in epiya_motifs.items():
                    if caga_seq[i : i + 5] in motifs:
                        this_seg = seg
                        break
            this_motif = ""
            for motif, amino_acids in epiya_4aa.items():
                if caga_seq[i + 5 : i + 9] in amino_acids:
                    this_motif = motif
                    found_motifs.append(f"{this_motif}{this_seg}")
    return "".join(found_motifs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="epiya.py", description="EPIYA motif finder")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-s", "--seq", help="Single cagA sequence as argument")
    input_group.add_argument(
        "-f",
        "--file",
        help="FASTA file containing one or more cagA sequences",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "--sep",
        help="Separator for result output. Using ',' is great for CSV files",
        default="\t",
    )
    parser.add_argument(
        "-nr",
        "--norareseg",
        help="Make rare patterns such as B', B'', B''' appear as B",
        action="store_true",
    )
    args = parser.parse_args()
    if args.file:
        for record in SeqIO.parse(args.file, "fasta"):
            print(f"{record.id}{args.sep}{search_motif(record.seq, args.norareseg)}")
    if args.seq:
        print(search_motif(args.seq))
