from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer('task-tracker',
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

