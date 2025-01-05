import unittest
from unittest.mock import patch
from src.preprocess_graph import preprocess_graph  # Update import path if needed
import sys
from src.main_pipeline import pipeline
from src.graph_search import run_a_star
from src.graph_utils import library_function
from src.graph_utils import load_graph
from src.graph_search import bfs

sys.path.append("C:/Users/SEVEN/OneDrive/Desktop/stock/stock2/src")

class TestPipeline(unittest.TestCase):
    def test_bfs(self):
        graph = {0: [1, 2], 1: [2], 2: []}
        self.assertTrue(bfs(graph, 0, 2))  # Should find path from 0 to 2
        self.assertFalse(bfs(graph, 0, 3))  # Should not find path from 0 to 3
    
    def test_preprocess_graph(self):
        nodes, edges = ['A', 'B'], [['A', 'B', 1]]
        processed_nodes, processed_edges = preprocess_graph(nodes, edges)
        self.assertEqual(processed_nodes, [0, 1])  # Mapping of nodes to integers
        self.assertEqual(processed_edges, [(0, 1, 1)])  # Correct edge transformation

if __name__ == "__main__":
    unittest.main()

class TestFullPipeline(unittest.TestCase):
    def test_pipeline_valid_data(self):
        # Assuming pipeline() function handles graph processing, algorithm execution, and result output
        try:
            pipeline('valid_graph.json', 0, 2, 'A*')
            print("Pipeline executed successfully.")
        except Exception as e:
            self.fail(f"Pipeline failed: {e}")

    def test_pipeline_invalid_data(self):
        try:
            pipeline('invalid_graph.json', 0, 2, 'A*')  # This file does not exist
            self.fail("Pipeline should have failed due to missing input file.")
        except Exception as e:
            print(f"Pipeline failed as expected: {e}")

if __name__ == "__main__":
    unittest.main()

class TestSearchLibrary(unittest.TestCase):
    @patch('src.some_module.run_a_star')  # Update the import path if necessary
    def test_run_a_star(self, mock_a_star):
        mock_a_star.return_value = ['A', 'B', 'C']
        graph = load_graph('valid_graph.json')
        result = run_a_star(library_function, graph, 'A', 'C')
        self.assertEqual(result, ['A', 'B', 'C'])
