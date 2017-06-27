import random
import networkx as nx

from .data import Person

MARRIAGE = 'marriage'
FATHER = 'father'
MOTHER = 'mother'

def make_family_tree(generations, size):
    # This generates a geneology by selecting an initial seed population
    # The members of that are then paired up with marriages
    # The paired members then have babies
    # The babies form the next round
    # This is heavily simplified OBVIOUSLY

    family_tree = nx.MultiDiGraph()
    if generations <= 0 or size <= 0:
        return family_tree

    pairs = _add_ancestors(family_tree, size)
    parents = pairs

    for _ in range(generations - 1):
        parents = _add_generation(family_tree, parents, size)

    return family_tree

def _add_ancestors(graph, size):
    people = [Person.make() for _ in range(size)]
    graph.add_nodes_from(people)

    pairs = _pair_off(people)
    for pair in pairs:
        graph.add_edge(pair[0], pair[1], key=MARRIAGE)
        graph.add_edge(pair[1], pair[0], key=MARRIAGE)

    return pairs

def _add_generation(graph, parents, size):
    if not parents:
        return []

    births = [(Person.make(), couple) for couple in random.choices(parents, k=size)]
    for birth in births:
        graph.add_edge(birth[0], birth[1][0], key=FATHER)
        graph.add_edge(birth[0], birth[1][1], key=MOTHER)

    return _pair_off(birth[0] for birth in births)

def _pair_off(people):
    boys = [person for person in people if person.is_male()]
    girls = [person for person in people if person.is_female()]

    return list(zip(boys, girls)) # so arbitrary
