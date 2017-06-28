from lib.subgraph import find_all_subgraphs, replace_subgraph
from .data import EXPRESSION_SUBSTITUTIONS

def expand(graph):
    # Have fun
    yield graph

    for expression, substitutions in EXPRESSION_SUBSTITUTIONS.items():
        for subgraph, mapping in find_all_subgraphs(graph, expression):
            for substitution in substitutions:
                expansion = replace_subgraph(graph, subgraph, mapping, substitution)
                for hell in expand(expansion):
                    yield hell
