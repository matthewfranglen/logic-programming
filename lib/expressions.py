"""
Expressions form the search which can be applied to the Fact graph.

The aim is to represent the search as an expression.
An expression is formed of placeholders, relationships and established values.

Placeholders represent values which are yet to be determined.
Without the constraint applied by relationships, all people are valid for a given placeholder.

Relationships represent connections between people.
Relationships can be substituted by compatible expressions.
This substitution can be infinite, so relationship expansion is handled by generators.

Established values are reified placeholders.
They only match a single person.
"""

import abc

class Value:

    def __init__(self, label, *values):
        self.label = label
        self.values = values

    def reify(self, values):
        """ This returns a reduced value which is the intersection of the two values """
        intersection = set(self.values).intersection(values)
        return Value(self.label, *intersection)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        """ This allows reify to work over any iterable by making Value an iterable """
        return iter(self.values)

    def __repr__(self):
        return f'Value({self.label}, {self.values})'


class Expression(abc.ABC):

    @abc.abstractmethod
    def expand(self):
        """ This transforms the expression into other expressions that are equivalent """
        pass

    @abc.abstractmethod
    def resolve(self, events, people):
        """ This attempts to apply the expression to return valid answers from the args sets """
        pass

class ParentExpression(Expression):

    def __init__(self, children, parents):
        self.parents = parents
        self.children = children

    def expand(self):
        return [ChildExpression(self.parents, self.children)]

    def resolve(self, events, people):
        return []

    def __repr__(self):
        return f'get_parents({self.children}) intersected with {self.parents}'

class ChildExpression(Expression):

    def __init__(self, parents, children):
        self.parents = parents
        self.children = children

    def expand(self):
        return []

    def resolve(self, events, people):
        for parent in self.parents:
            children = self.children.reify(get_children(events, people, parent))
            if children:
                yield (parent, children)

    def __repr__(self):
        return f'get_children({self.parents}) intersected with {self.children}'

def get_children(events, _, parent):
    return set(
        event.child
        for event in events
        if event.type == 'birth'
        and parent in event.parents
    )

# get_partners
