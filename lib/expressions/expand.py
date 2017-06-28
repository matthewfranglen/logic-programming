from lib.subgraph import find_all_subgraphs, replace_subgraph
from .data import EXPRESSION_SUBSTITUTIONS

def expand(graph):
    # Have fun

    to_do = [graph]
    for expression_graph in to_do:
        yield expression_graph

        for expression, substitutions in EXPRESSION_SUBSTITUTIONS.items():
            for application in _apply_expression_substitutions(
                    expression_graph, expression, substitutions
            ):
                to_do.append(application)

def _apply_expression_substitutions(graph, expression, substitutions):
    for subgraph, mapping in find_all_subgraphs(graph, expression):
        for substitution in substitutions:
            yield replace_subgraph(graph, subgraph, mapping, substitution)
