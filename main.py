from additional_modules.dna_rna_tools import (
    is_nucleic_acid, transcribe, reverse, complement, reverse_complement
)
from additional_modules.module_filter_fastq import (
    calculate_gc_content, check_sequence_length, quality_check, input_check
)


def run_dna_rna_tools(*args):
    """
    Function for converting nucleic acid sequences. Available transformations:
    Nucleic acid affiliation testing - is_nucleic_acid(),transcription - transcribe(),
    reversal - reverse(), complementary sequence display - complement(), complementary
    sequence reversal - reverse_complement().

    Arguments:
    *args: seqs
    *sequences, procedure = args

    Returns bool or string according to the used function.
    """

    if not args:
        return False
    *sequences, procedure = args

    available = {
        "is_nucleic_acid": is_nucleic_acid,
        "transcribe": transcribe,
        "reverse": reverse,
        "complement": complement,
        "reverse_complement": reverse_complement,
    }

    if procedure not in available:
        print("Unknown procedure")
        return None

    function = available[procedure]
    results = [function(sequence) for sequence in sequences]

    if len(results) == 1:
        return results[0]
    return results


def filter_fastq(
    seqs, gc_bounds=(0, 100), length_bounds=(0, 2**32), quality_threshold: int = 0
):
    """
    Checks sequences from a dictionary for compliance with specified requirements.

    Arguments:
    seqs: dict
    gc_bounds=(0, 100)
    length_bounds=(0, 2**32)
    quality_threshold: int = 0

    Returns a dictionary with sequences that match the requirements.
    """

    if not input_check(seqs, gc_bounds, length_bounds, quality_threshold):
        return None

    if isinstance(gc_bounds, (int, float)):
        gc_min, gc_max = 0, float(gc_bounds)
    else:
        gc_min, gc_max = gc_bounds


    if isinstance(length_bounds, (int, float)):
        len_min, len_max = 0, int(length_bounds)
    else:
        len_min, len_max = length_bounds

    filtered_seqs = {}

    for name, (sequence, quality) in seqs.items():

        if not is_nucleic_acid(sequence):
            continue

        gc_content = calculate_gc_content(sequence)

        if not (gc_min <= gc_content <= gc_max):
            continue

        if not check_sequence_length(sequence, (len_min, len_max)):
            continue

        if not quality_check(quality, quality_threshold):
            continue

        filtered_seqs[name] = (sequence, quality)

    return filtered_seqs
