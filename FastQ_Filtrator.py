from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import os


def filter_fastq(input_file: str, output_file=None, gc_bounds=(0, 100),
    length_bounds=(0, 2**32), quality_threshold=0) -> None:
    """
    Filter FASTQ file based on GC content, sequence length, and quality
    Arguments:
    input_file: Path to input FASTQ file
    output_file: Path to output filtered FASTQ file
    gc_bounds (tuple or int): GC content bounds or single value as upper bound
    length_bound (tuple or int): Sequence length bounds or single value as upper bound
    quality_threshold (tuple or int): Minimum average Phred quality score
    """
    if isinstance(gc_bounds, (int)):
        gc_bounds = (0, gc_bounds)
    if isinstance(length_bounds, int):
        length_bounds = (0, length_bounds)
    
    gc_min, gc_max = gc_bounds
    len_min, len_max = length_bounds

    if output_file is None:
        base_name = os.path.basename(input_file)
        name_without_ext = os.path.splitext(base_name)[0]
        output_file = f"{name_without_ext}_filtered.fastq"

    if os.path.dirname(output_file) == "":
        output_file = os.path.join("filtered", output_file)
    
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filtered_records = []

    for record in SeqIO.parse(input_file, "fastq"):

        sequence = str(record.seq)
        record_id = record.id
        record_description = record.description
        qualities = record.letter_annotations.get("phred_quality", [])

        if not (len_min <= len(sequence) <= len_max):
            continue

        gc_content = gc_fraction(record.seq)
        if not (gc_min <= gc_content <= gc_max):
            continue

        if qualities:
            avg_quality = sum(qualities) / len(qualities)
            if avg_quality < quality_threshold:
                continue

        filtered_records.append(record)

    if filtered_records:
        SeqIO.write(filtered_records, output_file, "fastq")

    return len(filtered_records)