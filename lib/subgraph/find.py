def find_all_subgraphs(graph, match):
    """
    This finds all matching subgraphs within the graph.
    The subgraphs are returned as a derived graph based on the node list, so
    all edges are present - even ones not present in match.

    The subgraph is matched by edge label only. All of the edges must be
    present in the subgraph, however nodes that are distinct in the match are
    not required to be distinct in the match.
    """
    if not match:
        return []

    return _find(graph, match, {}, match)

def _find(graph, match, mapping, unmapped):
    """
    This recursively finds matches by processing one unmapped node per call.

    When the corresponding node for the unmapped node can be found the search
    can proceed. An eligible node in the graph has the same edges to the mapped
    nodes as the match does.
    """
    if not unmapped:
        return [graph.subgraph(mapping.values())]

    node, *remaining = unmapped
    mapped = set(mapping.keys())

    in_edges = [
        (mapping[edge[0]], edge[2]['label'])
        for edge in match.in_edges(node, data=True)
        if edge[0] in mapped
    ]
    out_edges = [
        (mapping[edge[1]], edge[2]['label'])
        for edge in match.out_edges(node, data=True)
        if edge[1] in mapped
    ]
    identity_edges = [
        edge[2]['label']
        for edge in match.edges(node, data=True)
        if edge[0] == edge[1]
    ]

    return (
        subgraph
        for graph_node in graph
        for subgraph in _find(graph, match, {node: graph_node, **mapping}, remaining)
        if _all_in_edges_present(graph, graph_node, in_edges)
        and _all_out_edges_present(graph, graph_node, out_edges)
        and _all_identity_edges_present(graph, graph_node, identity_edges)
    )

def _all_in_edges_present(graph, graph_node, in_edges):
    graph_edges = [
        (edge[0], edge[2]['label'])
        for edge in graph.in_edges(graph_node, data=True)
    ]
    return all(edge in graph_edges for edge in in_edges)

def _all_out_edges_present(graph, graph_node, out_edges):
    graph_edges = [
        (edge[1], edge[2]['label'])
        for edge in graph.out_edges(graph_node, data=True)
    ]
    return all(edge in graph_edges for edge in out_edges)

def _all_identity_edges_present(graph, graph_node, identity_edges):
    graph_edges = [
        edge[2]['label']
        for edge in graph.edges(graph_node, data=True)
        if edge[0] == edge[1]
    ]
    return all(edge in graph_edges for edge in identity_edges)
