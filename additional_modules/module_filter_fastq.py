def calculate_gc_content(sequence: str) -> float:
    sequence = sequence.upper()
        gc_count = sequence.count('G') + sequence.count('C')
        total_length = len(sequence)

        if total_length == 0:
            return 'No sequence'

    return (gc_count / total_length) * 100

def check_sequence_length(sequence: str, length_bounds = (0, 2**32)) -> bool:
    seq_length = len(sequence)
    if isinstance(length_bounds,(int, float)):
        return 0 <= seq_length <= length_bounds
    else:
        lower, upper =  length_bounds
        return lower <= seq_length <= upper

def quality_check(quality: str, quality_threshold: int = 0) -> bool:
    qual_length = len(quality)
    n_bad_symbol = 0

    for char in quality:
        quality_scores = ord(char) - 33
        if quality_scores < quality_threshold:
            n_bad_symbol += 1

    return n_bad_symbol < qual_length
