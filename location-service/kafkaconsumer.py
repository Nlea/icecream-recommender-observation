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
            if message.key is not None and message.value is not None:
                headers = message.headers
                if headers is not None:
                    header_dict = {header_key: header_value for header_key, header_value in headers}
                    #print(f'this is the header from consume &{header_dict}')
                    #for header_key, header_value in headers:
                        #print(f"{header_key}: {header_value}")

                yield message.value.decode('utf-8'), message.key.decode('utf-8'), header_dict
        else:
            yield None, None, None

    
    


    def close(self):
        self.consumer.close()