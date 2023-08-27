from ...schema_registry.python.event import Event

from app.db import Session, User


async def handle_user_created(event: Event):
    version = event.dict['event_version']
    match version:
        case 1:
            await handle_user_created_v1(event)
        case _:
            raise NotImplementedError(f'user_created event version {version}')


async def handle_user_created_v1(event: Event):
    session = Session()
    new_user_entry = User(
        id=event.dict['data']['id'],
        role=event.dict['data']['role']
    )
    session.add(new_user_entry)
    session.commit()
