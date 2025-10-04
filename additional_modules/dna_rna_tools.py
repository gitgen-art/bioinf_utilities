def is_nucleic_acid(sequence: str) -> bool:
    unique_nucleotides = set(sequence.upper())

    dna_bases = set('ATGC')
    rna_bases = set('AUGC')

    result = (
        unique_nucleotides <= dna_bases) or (
        unique_nucleotides <= rna_bases)
    return result

def transcribe(sequence: str) -> str:
    if not is_nucleic_acid(sequence):
        print('It is not sequence of nucleotides')
        return None

    seq_upper = sequence.upper()
    if 'U' in seq_upper:
        print('Sequence is RNA')
        return None

    result = []
    for ch in sequence:
        if ch == "T":
            result.append("U")
        elif ch == "t":
            result.append("u")
        else:
            result.append(ch)
    return "".join(result)

def reverse(sequence: str) -> str:
    if not is_nucleic_acid(sequence):
        print('It is not sequence of nucleotides')
        return None
    return sequence[::-1]

def complement(sequence: str) -> str:
    if not is_nucleic_acid(sequence):
        print('It is not sequence of nucleotides')
        return None

    ComplementMap = {
        "A": "T", "a": "t",
        "T": "A", "t": "a", 
        "U": "A", "u": "a",
        "C": "G", "c": "g",
        "G": "C", "g": "c",
    }
    return ''.join([ComplementMap[n] for n in sequence])

def reverse_complement(sequence: str) -> str:
    return reverse(complement(sequence))
