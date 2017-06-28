import networkx as nx

def replace_subgraph(graph, match, mapping, replacement):
    """
    This replaces the specific subgraph within the graph with the replacement
    according to the mapping.

    This works by:
        * Removing every edge in the graph which is present in the match
        * Adding every node that is in the replacement but missing from the match
        * Removing every node that is in the match but missing from the replacement.
          THIS BREAKS UNRELATED EDGES.
        * Adding every edge that is in the replacement
    """
    result = nx.MultiDiGraph(graph)

    result.remove_edges_from(match.edges(keys=True))

    for missing_node in (node for node in replacement if node not in mapping):
        graph_node = _Symbol()
        mapping[missing_node] = graph_node
        result.add_node(graph_node)

    result.remove_nodes_from(
        node
        for node in set(match).difference(
            mapping[replacement_node] for replacement_node in replacement
        )
    )

    for source, destination, key in _to_graph_edges(mapping, replacement):
        result.add_edge(source, destination, key=key)

    return result

def _to_graph_edges(mapping, graph):
    return (
        (mapping[edge[0]], mapping[edge[1]], edge[2])
        for edge in graph.edges(keys=True)
    )

class _Symbol:
    """
    This represents a node added to a graph.

    The requirements are that:
        * Two separate instances of this not equal each other
          i.e. _Symbol() != _Symbol()
        * Two separate instances of this ideally hash to different values
          i.e. hash(_Symbol()) != hash(_Symbol())
        * The same instance equals itself, and hashes to the same value

    Luckily the default behaviour of an empty class meets these requirements.

    This is named after the javascript Symbol type.
    """

    pass
