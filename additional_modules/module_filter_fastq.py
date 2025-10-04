def calculate_gc_content(sequence: str) -> float:
    sequence = sequence.upper()
        gc_count = sequence.count('G') + sequence.count('C')
        total_length = len(sequence)

        if total_length == 0:
            return 0.0

    return (gc_count / total_length) * 100
