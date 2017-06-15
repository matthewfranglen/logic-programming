"""
Facts form the graph of data points and relationships between them.

This generates a very simple family tree.
"""

import random
import faker

FAKE = faker.Faker()

def make_geneology(depth, width):
    # This generates a geneology by selecting an initial seed population
    # The members of that are then paired up with marriages
    # The paired members then have babies
    # The babies form the next round
    # This is heavily simplified OBVIOUSLY

    events, people = _make_ancestors(width)
    parents = people

    for _ in range(depth):
        generation_events, parents = _make_generation(parents, width)
        events += generation_events
        people += parents

    return (events, people)

def _make_ancestors(width):
    people = [
        Person.boy() if i % 2 == 0 else Person.girl()
        for i in range(width)
    ]
    events, _ = _pair_off(people)

    return (events, people)

def _make_generation(parents, width):
    marriages, pairs = _pair_off(parents)

    if not pairs:
        return marriages, []

    births = [
        BirthEvent.make(random.choice(pairs))
        for _ in range(width)
    ]

    return marriages + births, [birth.child for birth in births]

def _pair_off(people):
    boys = [person for person in people if person.is_male()]
    girls = [person for person in people if person.is_female()]

    if (not boys) or (not girls):
        return ([], [])

    pairs = list(zip(boys, girls)) # so arbitrary
    events = [MarriageEvent(couple) for couple in pairs]

    return (events, pairs)


class Person:

    @staticmethod
    def boy():
        return Person('male')

    @staticmethod
    def girl():
        return Person('female')

    @staticmethod
    def make():
        return Person(random.choice(['male', 'female']))

    def __init__(self, gender):
        self.gender = gender
        self.name = FAKE.name_male() if self.gender == 'male' else FAKE.name_female()

    def is_male(self):
        return self.gender == 'male'

    def is_female(self):
        return self.gender == 'female'

    def __repr__(self):
        return f'Person({self.gender}, {self.name})'

class Event:

    def __repr__(self):
        return 'Event()'

class MarriageEvent(Event):

    def __init__(self, couple):
        self.type = 'marriage'
        self.couple = couple

    def __repr__(self):
        return f'Event({self.type}, {self.couple})'

class BirthEvent(Event):

    @staticmethod
    def make(parents):
        return BirthEvent(parents, Person.make())

    def __init__(self, parents, child):
        self.type = 'birth'
        self.parents = parents
        self.child = child

    def __repr__(self):
        return f'Event({self.type}, {self.parents}, {self.child})'
