def find_subgraphs(graph, subgraph):
    """
    This finds all matching subgraphs within the graph provided.
    This returns an object that can be treated like a generator.
    If the subgraph is empty then no matches will be returned.
    """

    if not subgraph:
        return []

    starting_vertex, *remainder = subgraph.vertexes

    return (
        sg
        for graph_vertex in graph.vertexes
        for sg in _resolve_subgraph(
            graph, subgraph, {starting_vertex: graph_vertex}, remainder
        )
    )

def _resolve_subgraph(graph, subgraph, node_mapping, unmapped_subgraph_vertexes):
    """
    This iteratively resolves the unmapped subgraph vertexes by finding the
    relationships that exist between the mapped vertexes and the unmapped ones,
    one by one.

    It then searches for the same relationships between the selected vertex and
    the already mapped vertexes. When these can be satisfied it then continues
    with the reduction by calling itself.
    """

    if not unmapped_subgraph_vertexes:
        return node_mapping

    mapped_subgraph_vertexes = node_mapping.keys()
    vertex, *unmapped = unmapped_subgraph_vertexes
    incoming_edges = [
        edge
        for edge in subgraph.inverse_edges[vertex]
        if edge.start in mapped_subgraph_vertexes
    ]
    outgoing_edges = [
        edge
        for edge in subgraph.edges[vertex]
        if edge.end in mapped_subgraph_vertexes
    ]

    return (
        sg
        for graph_vertex in graph.vertexes
        for sg in _resolve_subgraph(
            graph, subgraph, {vertex: graph_vertex, **node_mapping}, unmapped
        )
        if all(
            graph.get_matching_edges(mapped_subgraph_vertexes[edge.start], graph_vertex, edge.label)
            for edge in incoming_edges
        )
        and all(
            graph.get_matching_edges(graph_vertex, mapped_subgraph_vertexes[edge.end], edge.label)
            for edge in outgoing_edges
        )
    )
