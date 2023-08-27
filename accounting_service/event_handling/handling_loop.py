import asyncio
from kafka import KafkaConsumer

from schema_registry.python.resolve_event import resolve_event
from event_handling.handlers import handle_task_created

USER_STREAM_CONSUMER = KafkaConsumer("tasks-stream")

EVENT_NAME_TO_HANDLER_MAPPING = {
    'task_created': handle_task_created
}


async def stream_handling_loop(consumer: KafkaConsumer):
    for message in consumer:
        print(message)
        event = resolve_event(message)
        event.validate()
        handler_function = EVENT_NAME_TO_HANDLER_MAPPING[event.name]
        await handler_function(event)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.wait([stream_handling_loop(USER_STREAM_CONSUMER)])