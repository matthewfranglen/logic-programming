def is_parent(events, people, child, parent):
    return bool([
        event
        for event in events
        if event['type'] == 'birth'
            and child == event['child']
            and parent in event['parents']
    ])
