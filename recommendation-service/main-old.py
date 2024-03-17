from kafkaconsumer import Consumer
from kafkaproducer import Producer
import json
import threading
from icecream import IcecreamRecommendation

def main():
    consumer_config = {
        'bootstrap_servers':'localhost:9092',
        'group_id': 'geo_weather_group',
        'auto_offset_reset': 'latest'

}
    
    producer_config = {
        'bootstrap_servers': 'localhost:9092'
    }
    input_topic1= 'icecream.recommender.input2'
    input_topic2= 'icecream.recommender.input'

    output_topic= 'icecream.recommendor.flavour'
    
    consumer1 = Consumer(input_topic1, consumer_config)
    consumer2 = Consumer(input_topic2, consumer_config)

    producer = Producer(producer_config)

    icecream_recommendor = IcecreamRecommendation()


    # Shared data structure to store messages temporarily
    messages = {}
    input ={}

    # Event to signal when messages with the same UUID are received
    event = threading.Event()

    def handle_messages(consumer, topic):

        for message in consumer.consume_messages():
            json_data = json.loads(message)
            uuid = json_data.get('uuid')
            input['uuid'] = uuid
            if topic == 'icecream.recommendor.weather':
                input['weather'] = json_data.get("weather")
            else:
                input['location']= json_data.get("location")
                input['mood'] = json_data.get("mood")
                input['dietRestrictions'] = json_data.get("dietRestrictions")

            messages.setdefault(uuid, {})[topic] = json_data

            # Check if messages with the same UUID from both topics are received
            if len(messages.get(uuid, {})) == 2:
                print(f'Messages with UUID {uuid} received from both topics.')

                # Perform your business logic here
                print(input)
                icecream_flavor_recommendation = icecream_recommendor.get_recommendation(**input)
                print(icecream_flavor_recommendation)
                output_message = {"recommendation": icecream_flavor_recommendation, "uuid": uuid}

                producer.send(output_topic, output_message)


                # Reset event after processing
                event.set()


    thread1 = threading.Thread(target=handle_messages, args=(consumer2, input_topic2))
    thread1.start()
    
    thread2 = threading.Thread(target=handle_messages, args=(consumer1, input_topic1))
    thread2.start()



    # Wait for threads to finish
    thread1.join()
    thread2.join()



if __name__ == "__main__":
    main()