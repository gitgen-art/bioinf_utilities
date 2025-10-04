from additional_modules.dna_rna_tools.py import *
from additional_modules.module_filter_fastq import *

def run_dna_rna_tools(*args):
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
        print('Unknown procedure')
        return None

    function = available[procedure]
    results = [function(sequence) for sequence in sequences]

    if len(results) == 1:
        return results[0]
    return results

