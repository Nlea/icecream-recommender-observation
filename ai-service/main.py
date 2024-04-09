
from kafkaconsumer import Consumer
from kafkaproducer import Producer
from icecream import IcecreamRecommendation
import json
import os

def main():
    # Kafka configuration
    consumer_config = {
        'bootstrap_servers': os.environ.get('KAFKA_BROKER_HOST', 'localhost:9092'),
        'group_id': 'geo_consumer_group',
        'auto_offset_reset': 'latest'
    }

    producer_config = {
        'bootstrap_servers': os.environ.get('KAFKA_BROKER_HOST', 'localhost:9092')
    }

    input_topic = 'icecream.recommender.joinedInput'
    output_topic = 'icecream.recommender.flavour'

    # Initialize consumer and producer
    consumer = Consumer(input_topic, consumer_config)
    producer = Producer(producer_config)

    icecream_recommendor = IcecreamRecommendation()


    #for message in consumer.consume_keys():
        #print(message)

    for message in consumer.consume_messages():
        print(message)
        key = bytes(message[1], 'utf-8')
        json_data = json.loads(message)
        buisnesskey = json_data.get('businesskey')
        print(buisnesskey)


        recommendation = icecream_recommendor.get_recommendation(**json_data)
        output_message ={"recommendation": recommendation, "businesskey": buisnesskey}



        print(output_message)

    


        producer.send(output_topic, key, output_message)


if __name__ == "__main__":
    main()