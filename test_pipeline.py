import unittest
from src.main_pipeline import main
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestPipeline(unittest.TestCase):
    def test_main_pipeline(self):
        try:
            main()
            self.assertTrue(True)  # Passes if no exception is raised
        except Exception as e:
            self.fail(f"Pipeline raised an exception: {e}")
