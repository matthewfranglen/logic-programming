import unittest
import networkx as nx

from lib.subgraph import replace_subgraph

GRAPH = nx.MultiDiGraph()
GRAPH.add_edge('a', 'b', key='s')
GRAPH.add_edge('a', 'b', key='t')

class TestReplaceSubgraph(unittest.TestCase):

    def test_empty_replace(self):
        match = nx.MultiDiGraph()
        mapping = {}
        replacement = nx.MultiDiGraph()

        result = replace_subgraph(GRAPH, match, mapping, replacement)

        self.assertGraphEqual(GRAPH, result)

    def test_remove_node(self):
        match = nx.MultiDiGraph()
        match.add_node(1)
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_node('b')

        self.assertGraphEqual(expected, result)

    def test_remove_edge(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, key='s')
        mapping = {1: 'a', 2: 'b'}
        replacement = nx.MultiDiGraph()
        replacement.add_nodes_from([1, 2])

        result = replace_subgraph(GRAPH, match, mapping, replacement)
        expected = nx.MultiDiGraph()
        expected.add_edge('a', 'b', key='t')

        self.assertGraphEqual(expected, result)

    def test_reverse_edge(self):
        match = nx.MultiDiGraph()
        match.add_edge(1, 2, key='s')
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
        match.add_node(1)
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
        match.add_nodes_from([1, 2])
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
        match.add_node(1)
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
        match.add_node(1)
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
        match.add_node(1)
        mapping = {1: 'a'}
        replacement = nx.MultiDiGraph()
        replacement.add_nodes_from([1, 2])
        expected = (len(GRAPH), len(GRAPH.edges()))

        replace_subgraph(GRAPH, match, mapping, replacement)
        result = (len(GRAPH), len(GRAPH.edges()))

        self.assertEqual(expected, result)

    def assertGraphEqual(self, expected, actual): # pylint: disable-msg=invalid-name
        # This is named in violation of PEP8 in order to be consistent with the unittest module
        self.assertSetEqual(set(expected), set(actual))
        self.assertSetEqual(set(expected.edges(keys=True)), set(actual.edges(keys=True)))

    def assertSymbolGraphEqual(self, expected, actual): # pylint: disable-msg=invalid-name
        """
        This handles the _Symbol class, which is intentionally opaque.

        This checks that all non symbol nodes, and edges between them, are valid.
        It then checks that there is the same number of mocked nodes as symbols.
        It then checks that every mocked edge has an equivalent symbol edge.
        """
        # This is named in violation of PEP8 in order to be consistent with the unittest module

        expected_nodes = [
            node
            for node in expected
            if not is_symbol(node)
        ]
        expected_edges = [
            edge
            for edge in expected.edges(keys=True)
            if not is_symbol_edge(edge)
        ]
        actual_nodes = [
            node
            for node in actual
            if not is_symbol(node)
        ]
        actual_edges = [
            edge
            for edge in actual.edges(keys=True)
            if not is_symbol_edge(edge)
        ]

        expected_symbol_nodes = [
            node
            for node in expected
            if is_symbol(node)
        ]
        expected_symbol_edges = [
            edge
            for edge in expected.edges(keys=True)
            if is_symbol_edge(edge)
        ]
        actual_symbol_nodes = [
            node
            for node in actual
            if is_symbol(node)
        ]
        actual_symbol_edges = [
            edge
            for edge in actual.edges(keys=True)
            if is_symbol_edge(edge)
        ]

        self.assertSetEqual(set(expected_nodes), set(actual_nodes))
        self.assertEqual(len(expected_symbol_nodes), len(actual_symbol_nodes))

        self.assertSetEqual(set(expected_edges), set(actual_edges))
        self.assertEqual(len(expected_symbol_edges), len(actual_symbol_edges))
        for edge in expected_symbol_edges:
            self.assertTrue(any(
                symbol_sensitive_edge_equals(edge, actual_edge)
                for actual_edge in actual_symbol_edges
            ), f'Check failed for {edge} in {actual_symbol_edges}')

def is_symbol(obj):
    return type(obj).__name__ == '_Symbol' or isinstance(obj, MockSymbol)

def is_symbol_edge(edge):
    return is_symbol(edge[0]) or is_symbol(edge[1])

def symbol_sensitive_equals(one, two):
    if is_symbol(one):
        return is_symbol(two)
    return one == two

def symbol_sensitive_edge_equals(one, two):
    return symbol_sensitive_equals(one[0], two[0])  \
        and symbol_sensitive_equals(one[1], two[1]) \
        and one[2] == two[2]

class MockSymbol:
    def __eq__(self, other):
        return isinstance(other, MockSymbol)

    def __hash__(self): # pylint: disable-msg=useless-super-delegation
        # MockSymbol needs to be hashable, but by defining __eq__ the default hash method goes away
        return super(MockSymbol, self).__hash__()

if __name__ == '__main__':
    unittest.main()
