import unittest
import os
import tempfile
import shutil
from Bio import SeqIO
from FastQ_Filtrator import filter_fastq, setup_logging

class TestFastQFiltrator(unittest.TestCase):
    """Tests for FastQ_Filtrator.py"""
    
    @classmethod
    def setUpClass(cls):
        """Create a new directory for tests"""
        cls.test_dir = tempfile.mkdtemp()
        cls.test_fastq = os.path.join(cls.test_dir, "test.fastq")
        
        current_dir = os.path.dirname(__file__)
        source_file = os.path.join(current_dir, "test.fastq")
        shutil.copy2(source_file, cls.test_fastq)
        
        cls.log_file = os.path.join(cls.test_dir, "test.log")
        cls.logger = setup_logging(cls.log_file)
    
    @classmethod
    def tearDownClass(cls):
        """Delete the temporary directory"""
        shutil.rmtree(cls.test_dir)
    
    def test_nonexistent_file_error(self):
        """Test for error when input file does not exist"""
        with self.assertRaises(FileNotFoundError):
            filter_fastq(
                os.path.join(self.test_dir, "nonexistent.fastq"),
                logger=self.logger
            )
    
    def test_file_read_write(self):
        """File reading and writing test"""
        output_file = os.path.join(self.test_dir, "output.fastq")
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            logger=self.logger
        )
        
        self.assertTrue(os.path.exists(output_file))

        records = list(SeqIO.parse(output_file, "fastq"))
        self.assertEqual(len(records), filtered_count)
    
    def test_gc_filtering(self):
        """GC-content filtration test"""
        output_file = os.path.join(self.test_dir, "gc_filtered.fastq")
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            gc_bounds=(20, 60),
            logger=self.logger
        )
        
        records = list(SeqIO.parse(output_file, "fastq"))
        
        for record in records:
            from Bio.SeqUtils import gc_fraction
            gc = gc_fraction(record.seq) * 100
            self.assertTrue(20 <= gc <= 60)
    
    def test_length_filtering(self):
        """Length filtration test"""
        output_file = os.path.join(self.test_dir, "length_filtered.fastq")
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            length_bounds=(20, 200),
            logger=self.logger
        )
        
        records = list(SeqIO.parse(output_file, "fastq"))
        
        for record in records:
            self.assertTrue(20 <= len(record.seq) <= 200)
    
    def test_quality_filtering(self):
        """Quality filtration test"""
        output_file = os.path.join(self.test_dir, "quality_filtered.fastq")
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            quality_threshold=30,
            logger=self.logger
        )
        
        records = list(SeqIO.parse(output_file, "fastq"))
        
        for record in records:
            qualities = record.letter_annotations.get("phred_quality", [])
            if qualities:
                avg_quality = sum(qualities) / len(qualities)
                self.assertGreaterEqual(avg_quality, 30)

    def test_combined_filtering(self):
        """Combined filtration test for all parameters"""
        output_file = os.path.join(self.test_dir, "combined_filtered.fastq")
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            gc_bounds=(20, 60),
            length_bounds=(20, 150),
            quality_threshold=25,
            logger=self.logger
        )
        
        records = list(SeqIO.parse(output_file, "fastq"))
        
        for record in records:
            from Bio.SeqUtils import gc_fraction
            gc = gc_fraction(record.seq) * 100
            self.assertTrue(20 <= gc <= 60)
            self.assertTrue(20 <= len(record.seq) <= 150)
            
            qualities = record.letter_annotations.get("phred_quality", [])
            if qualities:
                avg_quality = sum(qualities) / len(qualities)
                self.assertGreaterEqual(avg_quality, 25)
    
    def test_default_params(self):
        """Test with default parameters"""
        output_file = os.path.join(self.test_dir, "default.fastq")
        
        original_records = list(SeqIO.parse(self.test_fastq, "fastq"))
        original_count = len(original_records)
        
        filtered_count = filter_fastq(
            self.test_fastq,
            output_file,
            logger=self.logger
        )
        
        self.assertEqual(filtered_count, original_count)
    
    def test_logging_functionality(self):
        """Log-test"""
        self.assertTrue(os.path.exists(self.log_file))
        
        with open(self.log_file, 'r') as f:
            log_content = f.read()

        self.assertIn("INFO", log_content)

if __name__ == "__main__":
    unittest.main()