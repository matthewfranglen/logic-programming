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


def get_children(events, _, parent):
    return [
        event.child
        for event in events
        if event.type == 'birth'
        and parent in event.parents
    ]
