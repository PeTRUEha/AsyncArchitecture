from ...schema_registry.python.event import Event
from random import randrange
from app.db import Session, User


async def handle_task_created(event: Event):
    version = event.dict['event_version']
    match version:
        case 1:
            await handle_task_created_v1(event)
        case _:
            raise NotImplementedError(f'user_created event version {version}')


async def handle_task_created_v1(event: Event):
    session = Session()
    new_task_entry = Task(
        id=event.dict['data']['id'],
        cost=randrange(20, 40, 1)
    )
    session.add(new_task_entry)
    session.commit()
