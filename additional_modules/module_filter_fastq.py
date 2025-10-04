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

    if seq_length == 0:
        return "No sequence"

    return (gc_count / seq_length) * 100


def check_sequence_length(sequence: str, length_bounds=(0, 2**32)) -> bool:
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


def quality_check(quality: str, quality_threshold: int = 0) -> bool:
    """
    Checks the quality of the sequence to meet the requirements.

    Arguments:
    quality: str
    quality_threshold: int = 0

    Returns bool.
    """

    qual_length = len(quality)
    n_bad_symbol = 0

    for char in quality:
        quality_scores = ord(char) - 33
        if quality_scores < quality_threshold:
            n_bad_symbol += 1

    return n_bad_symbol < qual_length


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
