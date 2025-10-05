# bioinf_utilities
Utilities for DNA/RNA sequence analysis and FASTQ.

## What is it?
bioinf_utilities is a Python package that provides analysis of nucleic acid sequences.

## The structure
bioinf_utilities/
|- README.md
|- main.py # The main module
|- test.py # File for quick start
|- additional_modules/
    |- dna_rna_tools.py # DNA/RNA tools
    |- module_filter_fastq.py # Tool for filtrating FASTQ-sequences

### The main module ('main.py')
Contains functions 'run_dna_rna_tools()' and 'filter_fastq()'.
The first one accept any number of positional arguments, where the last one is the procedure 
from the file 'dna_rna_tools.py'.
The second one ('filter_fastq()') accept the dictionary {'name':('sequence', 'quality')} and
the requirements, which you can tune:
- gc_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 100); 
- length_bounds = (the upper bound or tuple/list of 2 elements), default value = (0, 2**32);
- quality_threshold: int = 0. 
'filter_fastq()' accesses the package 'module_filter_fastq.py'.

### File for quick start:
You can run the program as "python test.py" to see the result, and then try the command "nano test.py" 
for understandig of usage.

### DNA/RNA tools ('dna_rna_tools.py')
- 'is_nucleic_acid()' - Checks that the input is the nucleic acid.transcription
- 'transcribe()' - Converts с.DNA into RNA
- 'reverse()' - Mirrors the sequence
- 'complement()' - Completes the complementary sequence
- 'reverse_complement()' - Completes the complementary sequence and then reverses the sequence

### Tool for filtrating FASTQ-sequences ('module_filter_fastq.py')
- 'calculate_gc_content' - Calculates the amount of G and C in a nucleic acid sequence as a percentage
- 'check_sequence_length' - Checks whether the length of a sequence is within a given range
- 'quality_check' - Checks the quality of the sequence to meet the requirements
- 'input_check' - Checks that the input meets the requirements

# Requirements:
Python 3.6+
