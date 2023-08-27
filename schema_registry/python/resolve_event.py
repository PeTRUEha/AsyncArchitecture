from schema_registry.python import Event


def resolve_event(event_dict: dict):
    event_name = event_dict['event_name']
    for subclass in Event.__subclasses__():
        if subclass.name == event_name:
            return subclass(event_name)
    raise KeyError(event_name)