import asyncio
from kafka import KafkaConsumer

from app.db import User, Session

user_stream_consumer = KafkaConsumer("users-stream")


async def user_stream_loop():
    for message in user_stream_consumer:
        print(message)
        match message['event_name']:
            case 'user_created':
                user_data = message['data']
                new_user = User(
                    id=user_data['id'],
                    role=user_data['role']
                )
                session = Session()
                session.add(new_user)
                session.commit()
            case _:
                print(f"event {message['event_name']} is unknown")
        await asyncio.sleep(1)





if __name__ == "__main__":
    asyncio.wait([user_stream_loop()])