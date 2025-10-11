from additional_modules.dna_rna_tools import (is_nucleic_acid)
import os

def read_fastq(file_path: str) -> dict[str, tuple[str, str]]:
    """
    Read FASTQ-file and converts it to a dictionary.

    Arguments:
    file_path: str

    Returns dictionary {header: (sequence, quality)}
    Raises:
    FileNotFoundError: if the file does not exist.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError

    seqs = {}

    with open(input_fastq, 'r') as file:
        while True:
            name = file.readline().strip()
            if not name:
                break

            sequence = file.readline().strip()
            plus_line = file.readline().strip()
            quality = file.readline().strip()

            seqs[name] = (sequence, quality)

        return seqs


def is_sequence_valid(sequence: str) -> bool:
    """Check the validity of a sequence."""
    return bool(sequence) and is_nucleic_acid(sequence)


def calculate_gc_content(sequence: str) -> float:
    """
    Calculates the amount of G and C in a nucleic acid sequence as a percentage.

    Arguments:
    sequence: str

    Returns float.
    Raises exception if len(sequence) is 0.
    """

    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")
    seq_length = len(sequence)

    return (gc_count / seq_length) * 100


def is_gc_ok(sequence: str, gc_min: float, gc_max: float) -> bool:
    """Check the gc-content."""
    gc_content = calculate_gc_content(sequence)
    return gc_min <= gc_content <= gc_max


def is_length_ok(sequence: str, length_bounds=(0, 2**32)) -> bool:
    """
    Checks whether the length of a sequence is within a given range.

    Arguments:
    sequence: str
    length_bounds=(0, 2**32)

    Returns bool.
    """

    seq_length = len(sequence)
    lower, upper = length_bounds
    return lower <= seq_length <= upper


def is_quality_ok(quality: str, quality_threshold: int = 0) -> bool:
    """
    Checks the quality of the sequence to meet the requirements.

    Arguments:
    quality: str
    quality_threshold: int = 0

    Returns bool.
    """

    avg_quality = sum(ord(char) - 33 for char in quality) / len(quality)
    return avg_quality >= quality_threshold

    for char in quality:
        quality_scores = ord(char) - 33
        if quality_scores < quality_threshold:
            n_bad_symbol += 1


def input_check(
    seqs, gc_bounds=(0, 100), length_bounds=(0, 2**32), quality_threshold: int = 0
) -> bool:
    """
    Checks that the input meets the requirements.

    Arguments:
    seqs: dict
    gc_bounds=(0, 100)
    length_bounds=(0, 2**32)
    quality_threshold: int = 0

    Returns bool.
    """

    if not isinstance(seqs, dict):
        print("Invalid input")
        return False

    for name, value in seqs.items():
        if not isinstance(name, str) or not isinstance(value, tuple):
            print("Invalid input")
            return False
        sequence, quality = value
        if not isinstance(sequence, str) or not isinstance(quality, str):
            print("Invalid input")
            return False

    if isinstance(gc_bounds, (int, float)):
        if not (0 <= gc_bounds <= 100):
            print("Invalid input")
            return False
    elif isinstance(gc_bounds, (tuple, list)):
        gc_min, gc_max = gc_bounds
        if (not (0 <= gc_min <= 100) or
                not (0 <= gc_max <= 100) or
                gc_min > gc_max):
            print("Invalid input")
            return False
    else:
        print("Invalid input")
        return False

    if not (0 <= quality_threshold <= 41):
        print("Invalid input")
        return False

    return True
