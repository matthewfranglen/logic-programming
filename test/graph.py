import unittest

class GraphTestCase(unittest.TestCase):

    def assertGraphEqual(self, expected, actual): # pylint: disable-msg=invalid-name
        # This is named in violation of PEP8 in order to be consistent with the unittest module
        expected_edges = expected.edges(keys=True)
        actual_edges = actual.edges(keys=True)

        self.assertSetEqual(
            set(expected.edges(keys=True)),
            set(actual.edges(keys=True)),
            f'Edges different: {expected_edges} compared to {actual_edges}'
        )
        self.assertSetEqual(
            set(expected),
            set(actual),
            f'Nodes different: {list(expected)} compared to {list(actual)}'
        )

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

        self.assertSetEqual(
            set(expected_nodes),
            set(actual_nodes),
            f'Non Symbol Nodes different: {expected_nodes} compared to {actual_nodes}'
        )
        self.assertEqual(
            len(expected_symbol_nodes),
            len(actual_symbol_nodes),
            f'Symbol Nodes different: {expected_symbol_nodes} compared to {actual_symbol_nodes}'
        )

        self.assertSetEqual(
            set(expected_edges),
            set(actual_edges),
            f'Non Symbol Edges different: {expected_edges} compared to {actual_edges}'
        )
        self.assertEqual(
            len(expected_symbol_edges),
            len(actual_symbol_edges),
            f'Symbol Edges different: {expected_symbol_edges} compared to {actual_symbol_edges}'
        )
        for edge in expected_symbol_edges:
            self.assertTrue(
                any(
                    symbol_sensitive_edge_equals(edge, actual_edge)
                    for actual_edge in actual_symbol_edges
                ),
                f'Missing Symbol Edge: {edge} in {actual_symbol_edges}'
            )

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
