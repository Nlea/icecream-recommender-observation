from kafka import KafkaProducer
import json
from opentelemetry import trace



class Producer:
   
    def __init__(self, kafka_config):   
        self.producer = KafkaProducer(
            **kafka_config,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send(self, topic, key, message,ctx, header):
        tracer = trace.get_tracer(__name__)
        with tracer.start_span("send kafka message", context=ctx):
            print(f'this is the header for producing the kafka message ${header}')
            self.producer.send(topic, value=message, key=key, headers=header)

    def close(self):
        self.producer.close()

