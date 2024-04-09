from kafka import KafkaProducer
import json

class Producer:
    def __init__(self, kafka_config):
        
        self.producer = KafkaProducer(
            **kafka_config,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send(self, topic, key, message):
        self.producer.send(topic, value=message, key=key)

    def close(self):
        self.producer.close()