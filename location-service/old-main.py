
from kafkaconsumer import Consumer
from kafkaproducer import Producer
import geolocator
import json





def main():

    # Kafka configuration
        consumer_config = {
           'bootstrap_servers': 'localhost:9092',
           'group_id': 'geo_consumer_group',
           'auto_offset_reset': 'latest'
       }

        producer_config = {
        'bootstrap_servers': 'localhost:9092'
    }

        input_topic = 'icecream.recommender.location'
        output_topic = 'icecream.recommender.weather'


 
   

      
        consumer = Consumer(input_topic, consumer_config)
    
        producer = Producer(producer_config)
 
        for message in consumer.consume_messages():
                 headers_dict=message[2]
                 print(headers_dict)
                 headers_tuple = [(key, value) for key, value in headers_dict.items()]
                 print(type(headers_tuple))
                 print(headers_tuple)
            
                 #print(type(message))
                 key = bytes(message[1], 'utf-8')
                 #print(key)

                 json_data = json.loads(message[0])
                 location = json_data.get('location')
                 buisnesskey = json_data.get('buisnesskey') 
                 
                 
                 if not location:
                      output_message = {'latitude': None, 'longitude': None, 'buisnesskey': buisnesskey }
                      print('No location provided')
                 else:
                    try:
                        geo = geolocator.Geolocator(location)

                        output_message = geo.getLocationDetails(headers_dict)
                        output_message['businesskey'] = buisnesskey
                    except:
                        print('Typo in location name or location does not exist')
                        output_message = {'latitude': None, 'longitude': None, 'buisnesskey': buisnesskey }
        
                 print(output_message)
                 producer.send(output_topic, key, output_message, headers_tuple)
                 


if __name__ == "__main__":
    main()
