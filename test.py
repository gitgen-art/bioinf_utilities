from FastQ_Filtrator import filter_fastq
from Sequence_Transformator import (DNASequence, 
    RNASequence, AminoAcidSequence, NucleicAcidSequence)

result1 = filter_fastq(
    "fastq", gc_bounds=80, length_bounds=500, quality_threshold=0
)
print(result1)

result2 = filter_fastq(
    "fastq", gc_bounds=80, length_bounds=(1,5), quality_threshold=0
)
print(result2)


dna = DNASequence("ATGCGTAC")
print(f"DNA: {dna}")
print(f"Complement seq: {dna.complement()}")
print(f"Transcribed seq: {dna.transcribe()}")

rna = RNASequence("AUGCAUCG")
print(f"\nRNA: {rna}")
print(f"Complement seq: {rna.complement()}")

protein = AminoAcidSequence("MVLSPADK")
print(f"\nProtein: {protein}")
print(f"Lenght of protein: {len(protein)} aminoacids")
print(f"Lenght of: {protein.nucleotide_len()} nucleotides")
