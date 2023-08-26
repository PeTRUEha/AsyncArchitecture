import json
import time
import uuid
from abc import ABC
from pathlib import Path

from jsonschema import validate

EVENT_PRODUCER = 'auth_service'


required = [
    "event_id",
    "event_version",
    "event_name",
    "event_time",
    "producer",
    "data"
]


class Event(ABC):
    schema_path: str = None  # определяется наследниками
    name: str = None   # определяется наследниками
    version: int = None

    def __init__(self, **kwargs):
        self.dict = dict(
            event_id=str(uuid.uuid4()),
            event_version=self.version,
            event_name=self.name,
            event_time=str(time.time()),
            producer=EVENT_PRODUCER,
        )

    def validate(self):
        full_schema_path = Path(__file__).parents[3].joinpath(self.schema_path)
        schema = json.load(open(full_schema_path))
        validate(self.dict, schema)


class UserCreated(Event):
    schema_path: str = "schema_registry/auth/user_created/1.json"
    name = 'user_created'
    version = 1
    def __init__(self, **kwargs):
        super().__init__()
        self.dict['data'] = kwargs


if __name__ == "__main__":
    event = UserCreated(
        **{
            'id': 1,
            'fullname': "name lastname",
            'role': "ADMINISTRATOR",
            'email': 'mail@mail.mail',
            'password': 'password',
        }
    )
    event.validate()
