import asyncio

from kafka import KafkaProducer, KafkaConsumer
from json import dumps

producer = KafkaProducer(value_serializer=lambda x: dumps(x).encode('utf-8'))

