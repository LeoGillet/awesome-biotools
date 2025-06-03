#!/usr/bin/env python3
import argparse
import os
"""
sample,fastq_1,fastq_2,ref,host,roi,covered_bed
"""

DEFAULT_REF_GENOME = "/storage/Genomes/Mycoplasma/Genitalium/Mycoplasma_genitalium_G37"
DEFAULT_HOST_GENOME = "/storage/Genomes/Homo/sapiens/Homo_sapiens_GRCh38.p14.fasta"
DEFAULT_TARGETS = "/storage/Genomes/Mycoplasma/Genitalium/_IMAP_Amplicons/BEDmg_CAS"

def write_samplesheet(filepaths, samplesheet_f, ref, host, targets):
    samplesheet_f.write("sample,fastq_1,fastq_2,ref,host,roi,covered_bed\n")
    for (r1, r2) in filepaths:
        sample_name = os.path.basename(r1).replace('_R1.fastq.gz', '')
        samplesheet_f.write(
            f"{sample_name},{r1},{r2},{ref},{host},{targets},\n"
        )
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="samplesheet_creator.py")
    parser.add_argument('-r', '--ref', default=DEFAULT_REF_GENOME)
    parser.add_argument('-o', '--host', default=DEFAULT_HOST_GENOME)
    parser.add_argument('-t', '--targets', default=DEFAULT_TARGETS)
    parser.add_argument('-s', '--samplesheet', default='samplesheet.csv', type=argparse.FileType('w'))
    parser.add_argument('input_dir')
    
    args = parser.parse_args()
    if not os.path.isdir(args.input_dir):
        raise NotADirectoryError(f"Input argument does not point to a valid directory. input_dir:{args.input_dir}")
    
    if not os.path.isfile(args.ref + ".fasta"):
        raise NotADirectoryError(f"Reference genome fasta file does not exist. ref:{args.ref + '.fasta'}")
    
    if not os.path.isfile(args.host):
        raise NotADirectoryError(f"Host genome fasta file does not exist. ref:{args.host}")
    
    if not os.path.isfile(args.targets + ".bed"):
        raise NotADirectoryError(f"Targets bed file does not exist. ref:{args.targets + '.bed'}")
    
    files_in_directory = os.listdir(args.input_dir)
    if not files_in_directory:
        raise FileNotFoundError(f"Input directory is empty or permissions are insufficient. input_dir:{args.input_dir}")
    
    fastq_files_in_directory = [fp for fp in files_in_directory if fp.endswith('.fastq.gz')]
    if not fastq_files_in_directory:
        raise FileNotFoundError(f"No files with '.fastq.gz' extension found in directory. input_dir:{args.input_dir}")
    
    paired_files_in_directory = [
        (os.path.join(args.input_dir, fp), os.path.join(args.input_dir, fp.replace('R1', 'R2'))) 
        for fp in fastq_files_in_directory
        if 'R1' in fp and os.path.isfile(
            os.path.join(args.input_dir, fp.replace('R1', 'R2'))
        )
    ]
    print(f"Found {len(paired_files_in_directory)} paired files in directory.")
    print(f"Reference genome: {args.ref.split('/')[-1]}")
    print(f"Host genome: {args.host.split('/')[-1]}")
    print(f"Targets: {args.targets.split('/')[-1]}")
    
    write_samplesheet(paired_files_in_directory, args.samplesheet, args.ref, args.host, args.targets)
    