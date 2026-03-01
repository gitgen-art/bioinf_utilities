from abc import ABC, abstractmethod

class BiologicalSequence(ABC):
    """An abstract class that defines the following interface:
        Working with the len function
        Ability to retrieve elements by index and slice a sequence
        Pretty printout
        Ability to check the alphabet of a sequence for correctness"""
    
    def __init__(self, sequence: str):
        self._sequence = sequence.upper()
        if not self._check_alphabet():
            raise ValueError(f"The sequence is not correct.")
    
    def __len__(self) -> int:
        """Returns the length of a sequence"""
        return len(self._sequence)
    
    def __getitem__(self, index):
        """Ability to get elements by index and make slices"""
        if isinstance(index, int):
            return self._sequence[index]
        elif isinstance(index, slice):
            return self.__class__(self._sequence[index])
        else:
            raise TypeError(f"The index must be int or slice")
    
    def __str__(self) -> str:
        """A beautiful output for users"""
        return f"{self.__class__.__name__}: {self._sequence}"
    
    @abstractmethod
    def _check_alphabet(self) -> bool:
        """An abstract method for checking the alphabet of a sequence"""
        pass


class NucleicAcidSequence(BiologicalSequence):
    """This class implements the BiologicalSequence interface.
       This class has the complement, reverse, and reverse_complement methods"""
    
    def __init__(self, sequence: str):
        super().__init__(sequence)

    def _check_alphabet(self):
        """Nucleic acid alphabet check"""
        alphabet = getattr(self, '_alphabet', None)
        if alphabet is None:
            raise NotImplementedError(f"Alphabet isn`t defined")
        return all(base in alphabet for base in self._sequence)
    
    def complement(self):
        """Returns the complementary sequence. Uses the complementarity map
        from the child class"""
        complement_map = getattr(self, '_complement_map', None)
        if complement_map is None:
            raise NotImplementedError(f"Complement_map isn`t defined")
        
        complemented = ''.join(complement_map[base] for base in self._sequence)
        return self.__class__(complemented)
    
    def reverse(self):
        """Returns the reverse sequence"""
        return self.__class__(self._sequence[::-1])
    
    def reverse_complement(self):
        """Returns the reverse complementary sequence"""
        return self.reverse().complement()


class DNASequence(NucleicAcidSequence):
    """Class for DNA sequences"""
    _alphabet = {'A', 'T', 'G', 'C'}
    _complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    
    def transcribe(self):
        """Transcribes DNA into RNA"""
        rna_sequence = self._sequence.replace('T', 'U')
        return RNASequence(rna_sequence)


class RNASequence(NucleicAcidSequence):
    """Class for RNA sequences"""
    _alphabet = {'A', 'U', 'G', 'C'}
    _complement_map = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}


class AminoAcidSequence(BiologicalSequence):
    """Class for Aminoacid sequences"""
    _alphabet = set('ACDEFGHIKLMNPQRSTVWY')
    
    def _check_alphabet(self) -> bool:
        """Checks that all characters belong to the amino acid alphabet"""
        return all(aa in self._alphabet for aa in self._sequence)
    
    def nucleotide_len(self) -> int:
        """Calculates the length of the template nucleotide sequence"""
        return len(self._sequence) * 3