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
    version: int = None

    @classmethod
    def from_data(cls, data: dict):
        event = cls()
        event.dict['data'] = data
        event.fill_defaults()
        return event

    def fill_defaults(self):
        self.dict.update(
            event_id=str(uuid.uuid4()),
            event_version=self.version,
            event_name=self.name,
            event_time=str(time.time()),
            producer=EVENT_PRODUCER,
        )

    def __init__(self, event_dict: dict = None):
        self.dict = event_dict if event_dict else {}

    def validate(self):
        full_schema_path = Path(__file__).parents[3].joinpath(self.schema_path)
        schema = json.load(open(full_schema_path))
        validate(self.dict, schema)
