import os.path
import csv
import random

BABY_NAMES = os.path.join(os.path.dirname(__file__), '..', 'data', 'baby-names.csv')

def make_geneology(depth, width):
    # This generates a geneology by selecting an initial seed population
    # The members of that are then paired up with marriages
    # The paired members then have babies
    # The babies form the next round
    # This is heavily simplified OBVIOUSLY

    data = read_baby_data()
    events, people, pairs = _make_ancestors(data, width)

    for i in range(depth):
        next_generation = []

        for pair in pairs:
            p_events, p_babies = _procreate(data, *pair)
            events += p_events
            people += p_babies
            next_generation += p_babies

        marriages, pairs = _pair_off(next_generation)
        events += marriages

        if not pairs:
            return (events, people)

    return (events, people)

def _read_baby_data():
    with open(BABY_NAMES, 'r') as handle:
        reader = csv.DictReader(handle)
        return list(reader)

def _random_boy(data):
    return random.choice([v for v in data if v['sex'] == 'boy'])

def _random_girl(data):
    return random.choice([v for v in data if v['sex'] == 'girl'])

def _random_person(data):
    return random.choice(data)

def _make_ancestors(data, width):
    boys = [_random_boy(data) for v in range(width // 2)]
    girls = [_random_girl(data) for v in range(width // 2)]
    people = boys + girls

    events, pairs = _pair_off(people)

    return (events, people, pairs)

def _pair_off(people):
    boys = [boy for boy in people if boy['sex'] == 'boy']
    girls = [girl for girl in people if girl['sex'] == 'girl']

    if (not boys) or (not girls):
        return ([], [])

    pairs = list(zip(boys, girls)) # so arbitrary
    events = [('married', b, g) for (b, g) in pairs]

    return (events, pairs)

def _procreate(data, daddy, mummy):
    child = _random_person(data)
    event = ('born', child, daddy, mummy)

    return ([event], [child])
