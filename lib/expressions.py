def is_parent(events, people, child, parent):
    return bool([
        event
        for event in events
        if event['type'] == 'birth'
            and child == event['child']
            and parent in event['parents']
    ])

def is_ancestor(events, people, person, ancestor):
    pass

def is_descendant(events, people, person, descendant):
    return is_ancestor(events, people, descendant, person)

def is_sibling(events, people, person, sibling):
    pass
