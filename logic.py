#!/usr/bin/env python

import itertools
import networkx as nx

from lib.family_tree import make_family_tree
from lib.expressions import PARENT, CHILD, expand
from lib.subgraph import find_all_subgraphs

def main():
    family_tree = make_family_tree(10, 10)
    expression = nx.MultiDiGraph()
    expression.add_edge('a', 'b', key=PARENT)
    expression.add_edge('b', 'c', key=CHILD)

    print('Given Graph:')
    for source, destination, key in family_tree.edges(keys=True):
        print(f'\t{key}: {source} -> {destination}')
    print()

    print('Given Expression:', expression.edges(keys=True)) # pylint: disable-msg=unexpected-keyword-arg,line-too-long
    print()

    for solution in itertools.islice(solve(family_tree, expression), 10):
        print('Solution:')
        for key, mapping in sorted(solution.items()):
            print(f'\t{key} = {mapping}')

def solve(graph, expression):
    for expansion in expand(expression):
        for _, solution in find_all_subgraphs(graph, expansion):
            yield solution

if __name__ == '__main__':
    main()
