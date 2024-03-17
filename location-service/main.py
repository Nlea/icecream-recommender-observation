
from kafkaconsumer import Consumer
from kafkaproducer import Producer
import geolocator
import json
import os
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace



def main():
    print("Hello I have started")
        
        #Set tracer
    
    #trace._set_tracer_provider(TracerProvider, log=bool)
    #trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
      # Set tracer
    trace._set_tracer_provider(TracerProvider(),log=True)
    
    # Create a BatchSpanProcessor and pass it to add_span_processor
    span_processor = BatchSpanProcessor(OTLPSpanExporter())
    trace.get_tracer_provider().add_span_processor(span_processor)

    tracer = trace.get_tracer(__name__)
  

    # Kafka configuration
    consumer_config = {
           'bootstrap_servers': os.environ.get('KAFKA_BROKER_HOST', 'localhost:9092'),
           'group_id': 'geo_consumer_group',
           'auto_offset_reset': 'latest'
       }

    producer_config = {
            'bootstrap_servers': os.environ.get('KAFKA_BROKER_HOST', 'localhost:9092')
    }

   #Kafka topics
    input_topic = 'icecream.recommender.input'
    output_topic = 'icecream.recommender.weather'

   #Initiate Consumer and Producer   
    consumer = Consumer(input_topic, consumer_config)
    producer = Producer(producer_config)

    print(consumer)
 
    for message in consumer.consume_messages():
        headers_dict=message[2]
        headers_tuple = [(key, value) for key, value in headers_dict.items()]


        value = headers_dict['traceparent']
        value_string =value.decode('utf-8')
        carrier ={'traceparent':value_string}
        print(type(value))
        print(type(headers_dict))
        ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
        print(f'Receive context: ${ctx}')


        key = bytes(message[1], 'utf-8')
        

        json_data = json.loads(message[0])
        location = json_data.get('location')
        name = json_data.get('name')
        mood = json_data.get("mood")
        dietRestrictions = json_data.get("dietRestrictions")
        print(f'This is the location: {location}')
        buisnesskey = json_data.get('buisnesskey') 
                 
                 
        #with tracer.start_span("process message", context=ctx):
        if not location:
            output_message = {'latitude': None, 'longitude': None, 'buisnesskey': buisnesskey }
            print('No location provided')
        else:
            try:
                print(f'Location name: {location}')
                geo = geolocator.Geolocator(location)
                output_message = geo.getLocationDetails(ctx,headers_dict)
                output_message['businesskey'] = buisnesskey
                output_message['mood'] = mood
                output_message['name'] = name
                output_message['dietRestrictions']= dietRestrictions
                output_message['location'] = location
            except Exception as e:
                print(e)
                print('Typo in location name or location does not exist')
                output_message = {'latitude': None, 'longitude': None, 'buisnesskey': buisnesskey, 'dietRestrictions': dietRestrictions, 'mood': mood, 'name': name, 'location': location }
        
        print(output_message)
        with tracer.start_span("send-geo-data-message", context=ctx):
            producer.send(output_topic, key, output_message, ctx, headers_tuple)
                 


if __name__ == "__main__":
    main()
