#!/usr/bin/env python

import itertools
import lib.facts as facts
import lib.expressions as expressions

def main():
    events, people = facts.make_geneology(10, 10)

    parents = expressions.Value('parents', *people)
    children = expressions.Value('children', *people)
    is_parent = expressions.ParentExpression(children, parents)

    for solution in itertools.islice(solve(events, people, is_parent), 10):
        print(solution)

def solve(events, people, expression):
    return (
        resolution
        for expansion in expand(expression)
        for resolution in resolve(events, people, expansion)
    )

def resolve(events, people, expression):
    return expression.resolve(events, people)

def expand(expression):
    # TODO: Try to prevent cyclic expansions!
    yield expression

    for expansion in (
            v
            for e in expression.expand()
            for v in expand(e)
        ):
        yield expansion

if __name__ == '__main__':
    main()
