from schema_registry.python.event import Event


class UserCreated(Event):
    schema_path: str = "schemas/auth/user_created/1.json"
    name = 'user_created'
    default_version = 1


class TaskCreated(Event):
    schema_path: str = "schemas/auth/task_created/1.json"
    name = 'task_created'
    default_version = 1