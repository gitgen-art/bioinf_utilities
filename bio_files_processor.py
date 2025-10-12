import os


def convert_multiline_fasta_to_oneline(input_fasta: str, output_fasta: str = None) -> str:
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

    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        current_header = None
        current_sequence = []

        for line in infile:
            line = line.strip()

            if line.startswith('>'):

                if current_header is not None:

                    full_sequence = ''.join(current_sequence)
                    outfile.write(f"{current_header}\n{full_sequence}\n")

                current_header = line
                current_sequence = []
            else:

                if line:
                    current_sequence.append(line)

        if current_header is not None:
            full_sequence = ''.join(current_sequence)
            outfile.write(f"{current_header}\n{full_sequence}\n")
    return output_fasta
