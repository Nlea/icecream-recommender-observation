package com.nlea.icecream.weatherservice.kafka;


import com.nlea.icecream.weatherservice.domain.WeatherFetcher;
import com.nlea.icecream.weatherservice.config.KafkaConsumerConfig;
import com.nlea.icecream.weatherservice.config.KafkaProducerConfig;
//import dev.autometrics.bindings.Autometrics;
import dev.autometrics.bindings.Autometrics;
import io.micrometer.observation.Observation;
import io.micrometer.observation.ObservationRegistry;
import io.micrometer.observation.annotation.Observed;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;


//@Observed(name="KafkaHandler")
@Service
public class KafkaHandler {

    private final ObservationRegistry registry;
    private final KafkaTemplate<String,String> kafkaTemplate;
    private final KafkaConsumerConfig kafkaConsumerConfig;
    private final KafkaProducerConfig kafkaProducerConfig;
    private final WeatherFetcher weatherFetcher;

    KafkaHandler(ObservationRegistry registry, KafkaTemplate kafkaTemplate, KafkaConsumerConfig kafkaConsumerConfig, KafkaProducerConfig kafkaProducerConfig, WeatherFetcher weatherFetcher){
        this.registry =registry;
        this.kafkaTemplate = kafkaTemplate;
        this.kafkaConsumerConfig = kafkaConsumerConfig;
        this.kafkaProducerConfig = kafkaProducerConfig;
        this.weatherFetcher= weatherFetcher;
    }


    @Autometrics
    @KafkaListener(topics = "icecream.recommender.weather", groupId ="icecream-club")
    public void listen(@Payload String message, ConsumerRecord<String, String> record) {

        var observation = Observation.createNotStarted("consume-weather-event", registry).start();


        String key = record.key();
        System.out.println("Received Message in group foo: " + message);
        // Extract the value of the "description" field
        JSONObject jsonObject = new JSONObject(record.value());
        String businesskey = jsonObject.getString("businesskey");
        String name = jsonObject.getString("name");
        String mood = jsonObject.getString("mood");
        String location = jsonObject.getString("location");

        String dietRestrictions = jsonObject.getString("dietRestrictions");
        System.out.println(businesskey);
        try{
            Double longitude = jsonObject.getDouble("longitude");
            Double latitude = jsonObject.getDouble("latitude");

            String weather = weatherFetcher.getWeatherCondition(longitude,latitude);
            String jsonData ="{\"weather\":\"" + weather + "\",\"businesskey\":\"" + businesskey + "\", \"mood\":\"" + mood + "\", \"name\":\"" + name + "\", \"dietRestrictions\":\"" + dietRestrictions + "\", \"location\":\"" + location + "\" }";
            System.out.println(jsonData);


            observation.event(Observation.Event.of("weather info created"));
            observation.highCardinalityKeyValue("weather",weather);

            kafkaTemplate.send("icecream.recommender.joinedInput", key, jsonData);
              }catch (JSONException e){
            String weather = "no info";
            String jsonData ="{\"weather\":\"" + weather + "\",\"businesskey\":\"" + businesskey + "\", \"mood\":\"" + mood + "\", \"name\":\"" + name + "\", \"dietRestrictions\":\"" + dietRestrictions + "\", \"location\":\"" + location + "\" }";


            kafkaTemplate.send("icecream.recommender.joinedInput",key, jsonData);

        } finally {
            observation.stop();

            System.out.println("Done");
        }

        }


    }

