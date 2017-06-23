import unittest

from lib.graph import Graph, Edge, Vertex, find_subgraphs

GRAPH = Graph(
    [Vertex(None, 'a'), Vertex(None, 'b')],
    [Edge('a', 'b', 's'), Edge('a', 'b', 't')]
)

class TestSubgraphMatching(unittest.TestCase):

    def test_empty_subgraph(self):
        self.assertEqual(find_subgraphs(GRAPH, []), [])

    def test_single_vertex_subgraph(self):
        subgraph = Graph([Vertex(None, 'one')], [])
        matches = list(find_subgraphs(GRAPH, subgraph))
        self.assertEqual(matches, [{'one': 'a'}, {'one': 'b'}])

if __name__ == '__main__':
    unittest.main()
