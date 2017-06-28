import unittest
import networkx as nx

from test.graph import GraphTestCase, MockSymbol # pylint: disable-msg=wrong-import-order
from lib.expressions import FATHER, MOTHER, MARRIAGE, PARENT, CHILD, ANCESTOR, DESCENDANT, expand

class TestExpressionExpansion(GraphTestCase):

    def test_no_expression(self):
        expression = make_expression_graph()

        result = list(expand(expression))

        self.assertEqual([expression], result)

    def test_no_expand(self):
        expression = make_expression_graph(
            1, 2, FATHER,
            1, 3, MOTHER,
            2, 3, MARRIAGE,
            3, 2, MARRIAGE
        )

        result = list(expand(expression))

        self.assertEqual([expression], result)

    def test_single_expand(self):
        expression = make_expression_graph(1, 2, PARENT)

        result = list(expand(expression))
        expected = [
            make_expression_graph(1, 2, PARENT),
            make_expression_graph(1, 2, FATHER),
            make_expression_graph(1, 2, MOTHER)
        ]

        self.assertEqual(len(expected), len(result))
        for expect, actual in zip(expected, result):
            self.assertGraphEqual(expect, actual)

    def test_double_expand(self):
        expression = make_expression_graph(2, 1, CHILD)

        result = list(expand(expression))
        expected = [
            make_expression_graph(2, 1, CHILD),
            make_expression_graph(1, 2, PARENT),
            make_expression_graph(1, 2, FATHER),
            make_expression_graph(1, 2, MOTHER)
        ]

        self.assertEqual(len(expected), len(result))
        for expect, actual in zip(expected, result):
            self.assertGraphEqual(expect, actual)

    def test_infinite_ancestor_expand(self):
        expression = make_expression_graph(1, 2, ANCESTOR)

        result = expand(expression)

        for expected in [
                make_expression_graph(1, 2, ANCESTOR),
                make_expression_graph(1, 2, PARENT),
                make_expression_graph(1, 2, FATHER),
                make_expression_graph(1, 2, MOTHER)
        ]:
            self.assertGraphEqual(
                expected,
                result.__next__()
            )

        intermediary = MockSymbol()
        self.assertSymbolGraphEqual(
            make_expression_graph(1, intermediary, PARENT, intermediary, 2, ANCESTOR),
            result.__next__()
        )

    def test_infinite_descendant_expand(self):
        expression = make_expression_graph(2, 1, DESCENDANT)

        result = expand(expression)

        for expected in [
                make_expression_graph(2, 1, DESCENDANT),
                make_expression_graph(1, 2, ANCESTOR),
                make_expression_graph(1, 2, PARENT),
                make_expression_graph(1, 2, FATHER),
                make_expression_graph(1, 2, MOTHER)
        ]:
            self.assertGraphEqual(
                expected,
                result.__next__()
            )

        intermediary = MockSymbol()
        self.assertSymbolGraphEqual(
            make_expression_graph(1, intermediary, PARENT, intermediary, 2, ANCESTOR),
            result.__next__()
        )

def make_expression_graph(*edges):
    expression = nx.MultiDiGraph()
    edges_iter = iter(edges)

    # This use of zip groups the arguments into 3s
    for source, destination, key in zip(edges_iter, edges_iter, edges_iter):
        expression.add_edge(source, destination, key=key)

    return expression


if __name__ == '__main__':
    unittest.main()
