# bioinf_utilities
Utilities for DNA/RNA sequence analysis and FASTQ.

## What is it?
bioinf_utilities is a Python package that provides analysis of nucleic acid sequences.

## The structure
bioinf_utilities/
|- README.md
|- main.py # The main module
|- bio_files_processor.py # script for reading bioinf files
|- test.py # File for quick start
|- additional_modules/
    |- dna_rna_tools.py # DNA/RNA tools
    |- module_filter_fastq.py # Tool for filtrating FASTQ-sequences

### The main module ('main.py')
1. Contains functions 'run_dna_rna_tools()' and 'filter_fastq()'.
The first one accept any number of positional arguments, where the last one is the procedure 
from the file 'dna_rna_tools.py'.
Arguments:
    *args: seqs
    *sequences, procedure = argsArguments:

Example:
run_dna_rna_tools(example_dna, example_rna, "reverse")

2. The second one ('filter_fastq()') Converts FASTQ in a dictionary and checks sequences 
from a dictionary for compliance with specified requirements, which you can tune.

Arguments:
    input_fastq: str
    gc_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 100); 
    length_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 2**32);
    quality_threshold: int = 0. 

Note:'filter_fastq()' accesses the package 'module_filter_fastq.py'.

Example:
filtered_seqs = filter_fastq('./example_fastq.fastq')

### 'bio_files_processor.py'
A module for processing biological files containing functions for working with FASTA format
and analyzing BLAST results.
Functions
1. convert_multiline_fasta_to_oneline
Converts a FASTA file with multi-line sequences to a format with single-line sequences.

Arguments:
    input_fasta (str) - path to the input FASTA file
    output_fasta (str, optional) - path to the output FASTA file. If not specified, created
automatically with the suffix _oneline.fasta

Features:
Reads FASTA files where sequences (DNA/RNA/protein) may be split across multiple lines
Saves sequences in a new FASTA file where each sequence occupies exactly one line

Example:
convert_multiline_fasta_to_oneline("example.fasta", "single_line_sequences.fasta")

2. parse_blast_output
Parses BLAST output files to extract the best protein matches for each query sequence.

Arguments:
    input_file (str) - path to the BLAST results text file
    output_file (str) - path to the output file for saving protein names

Features:
Reads BLAST output text files
For each query sequence, finds the "Sequences producing significant alignments" section
Extracts the first entry from the "Description" column
Saves all protein names in a single column, sorted alphabetically

Example:
parse_blast_output("example_blast_results.txt", "top_blast_hits.txt")

### File for quick start:
You can run the program as "python test.py" to see the result, and then try the command "nano test.py" 
for understandig of usage.

### DNA/RNA tools ('dna_rna_tools.py')
1. 'is_nucleic_acid()' - Checks that the input is the nucleic acid.transcription
2. 'transcribe()' - Converts с.DNA into RNA
3. 'reverse()' - Mirrors the sequence
4. 'complement()' - Completes the complementary sequence
5. 'reverse_complement()' - Completes the complementary sequence and then reverses the sequence

Example of usage in the main function:
run_dna_rna_tools(example_dna, example_rna, "reverse")

### Tool for filtrating FASTQ-sequences ('module_filter_fastq.py')
1. 'calculate_gc_content' - Calculates the amount of G and C in a nucleic acid sequence as a percentage
2. 'is_gc_ok' - Checks whether the percentage of GC in sequence is within a given range
3. 'is_length_ok' - Checks whether the length of a sequence is within a given range
4. 'is_quality_ok' - Checks the quality of the sequence to meet the requirements
5. 'input_check' - Checks that the input meets the requirements
6. 'read_fastq' - Read FASTQ-file and converts it to a dictionary
7. 'write_fastq' - Write filtered sequences in new file 'output_fastq' in folder "filtered".
Makes a recording to an existing one
8. 'write_sequences' - Write converted sequences in file 'output_fastq' in folder "filtered".
Makes a recording to an existing one

Example:
filtered_seqs = filter_fastq('./example_fastq.fastq')
write_fastq(filtered_seqs, 'remove_file')

# Requirements:
Python 3.6+

#Contacts:
https://github.com/gitgen-art
siddy-d@yandex.ru
