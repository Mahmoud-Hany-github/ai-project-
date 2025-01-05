import unittest
from src.preprocess_graph import preprocess_graph

class TestPreprocessGraph(unittest.TestCase):
    def test_preprocess_graph(self):
        nodes, edges = ['A', 'B'], [['A', 'B', 1]]
        processed_nodes, processed_edges = preprocess_graph(nodes, edges)
        self.assertEqual(processed_nodes, [0, 1])  # Mapping of nodes to integers
        self.assertEqual(processed_edges, [(0, 1, 1)])  # Correct edge transformation
