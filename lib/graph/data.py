"""
This defines three data types:

Vertex: This is a Vertex of the Graph which is uniquely identified by a label.
    If two Nodes have the same label they are considered to be the same Vertex.

Edge: This is an Edge of the Graph, connecting two Vertexes.
    This identifies the Vertexes by label.

Graph: This is a collection of Vertexes and Edges.
    This is implemented as an Adjacency list.
"""

from collections import defaultdict
from functools import reduce

class Graph:

    def __init__(self, vertexes, edges):
        self.vertexes = reduce(
            lambda map, vertex: map.__setitem__(vertex.label, vertex),
            vertexes,
            {}
        )
        self.edges = reduce(
            lambda map, edge: map[edge.start].append(edge),
            edges,
            defaultdict(list)
        )
        self.inverse_edges = reduce(
            lambda map, edge: map[edge.end].append(edge),
            edges,
            defaultdict(list)
        )

    def get_vertex(self, vertex_label):
        return self.vertexes[vertex_label]

    def get_edges(self, vertex_label):
        return self.edges[vertex_label]

    def get_connected_vertexes(self, vertex_label, edge_label):
        return [
            edge.end
            for edge in filter_edges(self.edges.get(vertex_label, []), edge_label)
        ]

    def get_inverse_connected_vertexes(self, vertex_label, edge_label):
        return [
            edge.start
            for edge in filter_edges(self.edges.get(vertex_label, []), edge_label)
        ]

    def get_matching_edges(self, start_vertex_label, end_vertex_label, edge_label):
        return [
            edge
            for edge in self.edges
            if edge.start == start_vertex_label
            and edge.end == end_vertex_label
            and edge.label == edge_label
        ]

    def __len__(self):
        return len(self.vertexes)

def filter_edges(edges, edge_label):
    return [edge for edge in edges if edge.label == edge_label]

class Edge:

    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.label == other.label

class Vertex:

    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __eq__(self, other):
        return self.label == other.label
