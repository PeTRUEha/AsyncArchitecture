import json
import time
import uuid
from abc import ABC
from pathlib import Path

from jsonschema import validate

EVENT_PRODUCER = 'auth_service'


class Event(ABC):
    schema_path: str = None  # определяется наследниками
    name: str = None   # определяется наследниками
    default_version: int = None

    @classmethod
    def from_data(cls, data: dict):
        event = cls()
        event.dict['data'] = data
        event.fill_defaults()
        return event

    def fill_defaults(self):
        self.dict.update(
            event_id=str(uuid.uuid4()),
            event_version=self.default_version,
            event_name=self.name,
            event_time=str(time.time()),
            producer=EVENT_PRODUCER,
        )

    def __init__(self, event_dict: dict = None):
        self.dict = event_dict if event_dict else {}

    def validate(self):
        full_schema_path = Path(__file__).parents[1].joinpath(self.schema_path)
        schema = json.load(open(full_schema_path))
        validate(self.dict, schema)


class UserCreated(Event):
    schema_path: str = "schemas/auth/user_created/1.json"
    name = 'user_created'
    default_version = 1


class TaskCreated(Event):
    schema_path: str = "schemas/auth/task_created/1.json"
    name = 'task_created'
    default_version = 1


if __name__ == "__main__":
    event = UserCreated.from_data(
        {
            'id': 1,
            'fullname': "name lastname",
            'role': "ADMINISTRATOR",
            'email': 'mail@mail.mail',
            'password': 'password',
        }
    )
    event.validate()
