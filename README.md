# bioinf_utilities
Utilities for DNA/RNA sequence analysis and FASTQ filtration.

## What is it?
bioinf_utilities is a Python package that provides analysis of nucleic acid sequences.

## The structure
bioinf_utilities/
|- README.md
|- Sequence_Transformator.py # OOP module for working with sequences
|- FastQ_Filtrator.py # FASTQ File Filtering Tool
|- test.py # File for quick start
|- bio_files_processor.py  

## Quick Start
Run the program to see the result of both FASTQ filtering and sequence transformation:
```bash
python tests/test.py
```
Use `nano test.py` to understand the usage examples.

# Quick tests
To quickly test individual features of the FastQ_Filtrator.py function, use the following code:
```bash
python -m unittest discover tests -v
```
It creates a separate folder for test files and then deletes it. It allows you to check for the presence of the file to be analyzed, file reading and writing, testing individual filtering functions (GC content, length, quality) and their combined operation, filtering with default parameters, and the presence of informational messages (INFO) in the log file created when working with the file being analyzed.

### Sequence_Transformator.py
An object-oriented module for working with biological sequences.
Class Hierarchy:

BiologicalSequence (ABC)
|- NucleicAcidSequence
|   |-DNASequence
|   |-RNASequence
|
|- AminoAcidSequence


1. Class BiologicalSequence 
Defines common interface for all biological sequences:
__len__() - the length of a sequence
__getitem__() - to get elements by index and make slices
__str__() - beautiful output
_check_alphabet() - abstract method for alphabet validation

2. Сlass NucleicAcidSequence
Сlass for nucleic acids with methods:
complement() - get complementary sequence
reverse() - get reverse sequence
reverse_complement() - get reverse complementary sequence

3. Сlass DNASequence
DNA-specific class with method:
transcribe() - transcribe DNA to RNA

4. Сlass RNASequence
RNA-specific class with methods, which inherits from NucleicAcidSequence

5. Сlass AminoAcidSequence
Protein sequence class with method:
nucleotide_len() - length of template nucleotide sequence


### Sequence_Transformator.py
FASTQ file filtering tool using Biopython. Filters reads by GC content, sequence length, and quality.
Requirements:
```bash
pip install biopython
```
Arguments:
    input_fastq: str
    gc_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 100); 
    length_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 2**32);
    quality_threshold: int = 0. 

Example:
filtered_seqs = filter_fastq("fastq")

### bio_files_processor.py
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

# Requirements:
Python 3.6+

```bash
pip install biopython
```

#Contacts:
https://github.com/gitgen-art
siddy-d@yandex.ru
