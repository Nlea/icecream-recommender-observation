
from kafkaconsumer import Consumer
from kafkaproducer import Producer
from icecream import IcecreamRecommendation
import json
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace



def main():
        
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
           'bootstrap_servers': 'localhost:9092',
           'group_id': 'geo_consumer_group',
           'auto_offset_reset': 'latest'
       }

    producer_config = {
        'bootstrap_servers': 'localhost:9092'
    }

   #Kafka topics
    input_topic = 'icecream.recommender.joinedInput'
    output_topic = 'icecream.recommender.flavour'

   #Initiate Consumer and Producer   
    consumer = Consumer(input_topic, consumer_config)
    producer = Producer(producer_config)
 
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
        print(f'This is the location: {location}')
        buisnesskey = json_data.get('buisnesskey') 
        icecream_recommendor = IcecreamRecommendation

        recommendation = icecream_recommendor.get_recommendation(ctx,**json_data)
        output_message ={"recommendation": recommendation, "businesskey": buisnesskey}
        print(output_message)
                 

                 


if __name__ == "__main__":
    main()
