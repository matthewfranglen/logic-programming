import unittest
import networkx as nx

from test.graph import GraphTestCase, MockSymbol # pylint: disable-msg=wrong-import-order
from lib.subgraph import replace_subgraph

GRAPH = nx.MultiDiGraph()
GRAPH.add_edge('a', 'b', key='s')
GRAPH.add_edge('a', 'b', key='t')

class TestReplaceSubgraph(GraphTestCase):

    def test_empty_replace(self):
        match = nx.MultiDiGraph()
        mapping = {}
        replacement = nx.MultiDiGraph()

        result = replace_subgraph(GRAPH, match, mapping, replacement)

        self.assertGraphEqual(GRAPH, result)

    def test_remove_node(self):
        match = nx.MultiDiGraph()
        match.add_node('a')
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_node('b')

        self.assertGraphEqual(expected, result)

    def test_remove_edge(self):
        match = nx.MultiDiGraph()
        match.add_edge('a', 'b', key='s')
        mapping = {1: 'a', 2: 'b'}
        replacement = nx.MultiDiGraph()
        replacement.add_nodes_from([1, 2])

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='t')

        self.assertGraphEqual(expected, result)

    def test_reverse_edge(self):
        match = nx.MultiDiGraph()
        match.add_edge('a', 'b', key='s')
        mapping = {1: 'a', 2: 'b'}
        replacement = nx.MultiDiGraph()
        replacement.add_edge(2, 1, key='s')

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('b', 'a', key='s')
        expected.add_edge('a', 'b', key='t')

        self.assertGraphEqual(expected, result)

    def test_add_identity_edge(self):
        match = nx.MultiDiGraph()
        match.add_node('a')
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()
        replacement.add_edge(1, 1, key='id')

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='s')
        expected.add_edge('a', 'b', key='t')
        expected.add_edge('a', 'a', key='id')

        self.assertGraphEqual(expected, result)

    def test_add_edge(self):
        match = nx.MultiDiGraph()
        match.add_nodes_from(['a', 'b'])
        mapping = {1: 'a', 2: 'b'}
        replacement = nx.MultiDiGraph()
        replacement.add_edge(2, 1, key='u')

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='s')
        expected.add_edge('a', 'b', key='t')
        expected.add_edge('b', 'a', key='u')

        self.assertGraphEqual(expected, result)

    def test_add_node(self):
        match = nx.MultiDiGraph()
        match.add_node('a')
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()
        replacement.add_nodes_from([1, 2])

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='s')
        expected.add_edge('a', 'b', key='t')
        expected.add_node(MockSymbol())

        self.assertSymbolGraphEqual(expected, result)

    def test_add_node_and_edge(self):
        match = nx.MultiDiGraph()
        match.add_node('a')
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()
        replacement.add_edge(2, 1, key='u')

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='s')
        expected.add_edge('a', 'b', key='t')
        expected.add_edge(MockSymbol(), 'a', key='u')

        self.assertSymbolGraphEqual(expected, result)

    def test_argument_unaltered(self):
        match = nx.MultiDiGraph()
        match.add_node('a')
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()
        replacement.add_nodes_from([1, 2])
        expected = (len(GRAPH), len(GRAPH.edges()))

        replace_subgraph(GRAPH, match, mapping, replacement)
        result = (len(GRAPH), len(GRAPH.edges()))

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
