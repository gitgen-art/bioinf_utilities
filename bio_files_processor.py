import os


def convert_multiline_fasta_to_oneline(
    input_fasta: str, output_fasta: str = None
) -> str:
    """
    Convert multiline FASTA to single-line format.

    Arguments:
    input_fasta: str - path to input FASTA file
    output_fasta: str (optional) - path to output FASTA file
                 If not provided, creates automatic name

    Returns: str - path to created file
    """

    if output_fasta is None:
        base_name = os.path.splitext(input_fasta)[0]
        output_fasta = f"{base_name}_oneline.fasta"

    with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
        current_header = None
        current_sequence = []

        for line in infile:
            line = line.strip()

            if line.startswith(">"):

                if current_header is not None:

                    full_sequence = "".join(current_sequence)
                    outfile.write(f"{current_header}\n{full_sequence}\n")

                current_header = line
                current_sequence = []
            else:

                if line:
                    current_sequence.append(line)

        if current_header is not None:
            full_sequence = "".join(current_sequence)
            outfile.write(f"{current_header}\n{full_sequence}\n")
    return output_fasta


def parse_blast_output(input_file: str, output_file: str) -> None:
    """
    Parse BLAST output file and extract best match descriptions.

    Arguments:
    input_file: str - path to BLAST results file
    output_file: str - path to output file with protein names

    Reads BLAST output, extracts the best match description for each query,
    and saves sorted protein names to output file.
    """

    best_proteins = []

    with open(input_file, "r") as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if "Sequences producing significant alignments:" in line:
            i += 1

            while i < len(lines):
                current_line = lines[i].strip()

                if (
                    not current_line
                    or current_line.startswith("Description")
                    or "Scientific Name" in current_line
                    or current_line.startswith("---")
                    or current_line.startswith("==")
                    or current_line.startswith("RID")
                ):
                    i += 1
                    continue

                if current_line:
                    parts = [p for p in current_line.split("  ") if p.strip()]
                    if parts:
                        protein_description = parts[0].strip()
                        best_proteins.append(protein_description)

                i += 1
        i += 1

    best_proteins.sort()

    with open(output_file, "w") as out_file:
        for protein in best_proteins:
            out_file.write(protein + "\n")
