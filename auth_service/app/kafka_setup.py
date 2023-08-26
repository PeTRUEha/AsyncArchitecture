from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(value_serializer=lambda x: dumps(x).encode('utf-8'))