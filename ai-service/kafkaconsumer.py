from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, topic, consumer_config):
        self.topic = topic
        self.consumer_config = consumer_config
        self.consumer = KafkaConsumer(
            self.topic,
            **self.consumer_config
        )

    def consume_messages(self):
        for message in self.consumer:
            #print("Received message:", message.value.decode('utf-8'))
            yield message.value.decode('utf-8')

    def close(self):
        self.consumer.close()