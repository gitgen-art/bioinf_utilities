from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import os
import argparse
import logging
import sys

def setup_logging(log_file=None):
    """Setting up logging to a file"""
    logger = logging.getLogger('FastQ_Filter')
    logger.setLevel(logging.DEBUG)

    if log_file is None:
        log_file = "fastq_filter.log"

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    return logger

def filter_fastq(input_file: str, output_file=None, gc_bounds=(0, 100),
    length_bounds=(0, 2**32), quality_threshold=0, logger=None) -> int:
    """
    Filter FASTQ file based on GC content, sequence length, and quality
    Arguments:
    input_file: Path to input FASTQ file
    output_file: Path to output filtered FASTQ file
    gc_bounds (tuple or int): GC content bounds or single value as upper bound
    length_bound (tuple or int): Sequence length bounds or single value as upper bound
    quality_threshold (tuple or int): Minimum average Phred quality score
    """
    if logger is None:
        logger = logging.getLogger('FastQ_Filter')
    
    logger.info(f"Starting filtering: input={input_file}, gc={gc_bounds}, length={length_bounds}, quality={quality_threshold}")

    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
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
    
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filtered_records = []
    total_records = 0

    for record in SeqIO.parse(input_file, "fastq"):
        total_records += 1

        sequence = str(record.seq)
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

    SeqIO.write(filtered_records, output_file, "fastq")
    if filtered_records:
        logger.info(f"Filtering complete: kept {len(filtered_records)} of {total_records} records -> {output_file}")
    else:
        logger.warning(f"No records passed filtering criteria, empty file created: {output_file}")
    
    return len(filtered_records)

def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description='Filter fastq files by GC content, sequence length, and quality scores',
        epilog="""
        Examples:
            # Basic filtering: keep reads with GC 20-80%, length 100-500bp, quality >30
            %(prog)s input.fastq -o output.fastq -g 20-80 -l 100-500 -q 30

            # Keep only short reads (up to 200bp) with GC <50%, save log
            %(prog)s input.fastq -g 50 -l 200 --log filtered.log

            # No quality filtering (just by length and GC)
            %(prog)s sample.fastq -l 50-300 -g 30-60
        """
    )

    parser.add_argument('input_file', type=str, help='Input FASTQ file path (.fastq)')

    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output filtered fastq file path (default: input_filtered.fastq)')
    
    parser.add_argument('-g', '--gc_bounds', type=str, default='0-100',
                        help='GC content bounds as MIN-MAX or single value as MAX (default: 0-100)')
    
    parser.add_argument('-l', '--length_bounds', type=str, default='0-4294967296',
                        help='Sequence length bounds as MIN-MAX or single value as MAX (default: 0-4294967296)')
    
    parser.add_argument('-q', '--quality_threshold', type=float, default=0,
                        help='Minimum average Phred quality score (default: 0)')
    
    parser.add_argument('--log', type=str, default=None,
                    help='Log file path (default: fastq_filter.log)')
    
    args = parser.parse_args()
    
    logger = setup_logging(args.log)

    try:
        if '-' in args.gc_bounds:
            gc_min, gc_max = map(float, args.gc_bounds.split('-'))
            gc_bounds = (gc_min, gc_max)
        else:
            gc_bounds = float(args.gc_bounds)
    except ValueError:
        logger.error(f"Invalid gc_bounds format: {args.gc_bounds}. Use MIN-MAX or single value.")
        sys.exit(1)

    try:
        if '-' in args.length_bounds:
            len_min, len_max = map(int, args.length_bounds.split('-'))
            length_bounds = (len_min, len_max)
        else:
            length_bounds = int(args.length_bounds)
    except ValueError:
        logger.error(f"Invalid length_bounds format: {args.length_bounds}. Use MIN-MAX or single value.")
        sys.exit(1)

    try:
        filtered_count = filter_fastq(
            input_file=args.input_file,
            output_file=args.output,
            gc_bounds=gc_bounds,
            length_bounds=length_bounds,
            quality_threshold=args.quality_threshold,
            logger=logger
        )
        logger.info(f"Successfully filtered {filtered_count} sequences")
        
    except Exception as e:
        logger.error(f"Filtering failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()