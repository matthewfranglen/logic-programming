import unittest
import networkx as nx

from lib.subgraph import find_all_subgraphs

GRAPH = nx.MultiDiGraph()
GRAPH.add_edge('a', 'b', label='s')
GRAPH.add_edge('a', 'b', label='t')

class TestFindSubgraph(unittest.TestCase):

    def test_empty_graph(self):
        match = nx.MultiDiGraph()

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual([], subgraphs)

    def test_single_node(self):
        match = nx.MultiDiGraph()
        match.add_node(1)

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual([['a'], ['b']], subgraphs)

    def test_unconnected_nodes(self):
        match = nx.MultiDiGraph()
        match.add_nodes_from([1, 2])

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual([['a'], ['b', 'a'], ['a', 'b'], ['b']], subgraphs)

    def test_connected_nodes(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual(1, len(subgraphs))
        self.assertSetEqual(set(['a', 'b']), set(subgraphs[0]))

    def test_label_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='x')

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual([], subgraphs)

    def test_direction_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')
        match.add_edge(2, 1, label='t')

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual([], subgraphs)

    def test_multi_edge_filtering(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, label='s')
        match.add_edge(1, 2, label='t')

        subgraphs = [
            list(graph) for graph in find_all_subgraphs(GRAPH, match)
        ]
        self.assertEqual(1, len(subgraphs))
        self.assertSetEqual(set(['a', 'b']), set(subgraphs[0]))

if __name__ == '__main__':
    unittest.main()
