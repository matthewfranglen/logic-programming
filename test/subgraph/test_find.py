import unittest
import networkx as nx

from lib.subgraph import find_all_subgraphs

GRAPH = nx.MultiDiGraph()
GRAPH.add_edge('a', 'b', label='s')
GRAPH.add_edge('a', 'b', label='t')

def perform_find(match):
    return [
        (list(graph), mapping)
        for (graph, mapping) in find_all_subgraphs(GRAPH, match)
    ]

class TestFindSubgraph(unittest.TestCase):

    def test_empty_graph(self):
        match = nx.MultiDiGraph()

        result = perform_find(match)

        self.assertEqual([], result)

    def test_single_node(self):
        match = nx.MultiDiGraph()
        match.add_node(1)

        result = perform_find(match)
        expected = [
            (['a'], {1: 'a'}),
            (['b'], {1: 'b'})
        ]

        self.assertEqual(expected, result)

    def test_unconnected_nodes(self):
        match = nx.MultiDiGraph()
        match.add_nodes_from([1, 2])

        result = perform_find(match)
        expected = [
            (['a'], {1: 'a', 2: 'a'}),
            (['b', 'a'], {1: 'a', 2: 'b'}),
            (['a', 'b'], {1: 'b', 2: 'a'}),
            (['b'], {1: 'b', 2: 'b'})
        ]

        self.assertEqual(expected, result)

    def test_connected_nodes(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')

        result = perform_find(match)
        expected = [
            (['b', 'a'], {1: 'a', 2: 'b'})
        ]

        self.assertEqual(1, len(result))
        self.assertEqual(expected, result)

    def test_label_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='x')

        result = perform_find(match)

        self.assertEqual([], result)

    def test_direction_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')
        match.add_edge(2, 1, label='t')

        result = perform_find(match)

        self.assertEqual([], result)

    def test_multi_edge_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')
        match.add_edge(1, 2, label='t')

        result = perform_find(match)
        expected = [
            (['b', 'a'], {1: 'a', 2: 'b'})
        ]

        self.assertEqual(1, len(result))
        self.assertEqual(expected, result)

    def test_identity_edge_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 1, label='s')

        result = perform_find(match)

        self.assertEqual([], result)

if __name__ == '__main__':
    unittest.main()
