package com.nlea.icecream.inputservice.kafka;

import com.nlea.icecream.inputservice.domain.MessageReceiver;
import com.nlea.icecream.inputservice.domain.Recommendation;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class Consumer {

    @Autowired
    private MessageReceiver messageReceiver;

    @Autowired
    private Recommendation recommendation;

    @KafkaListener(topics = "icecream.recommender.flavour")
    public void listenGroupRecommend(ConsumerRecord<String, String> record) {


        System.out.println("Received Message in group foo: " + record.value());
        messageReceiver.setReceived(Boolean.TRUE);
        // Extract the value of the "description" field
        JSONObject jsonObject = new JSONObject(record.value());

        String content;

        try{

            //String recommendation = jsonObject.getString("recommendation");
            String businesskey = jsonObject.getString("businesskey");
            System.out.println(businesskey);

            content = jsonObject.getString("recommendation");
            if (businesskey.equals(messageReceiver.getBusniessKey())) {
                System.out.println("Keys are equal");
                recommendation.setContent(content);
                messageReceiver.setReceived(Boolean.TRUE);


            }
                //If match found, set receivedPayload




            }catch (JSONException e){
            //String uuid = "something";
            //String recommendation = "Sorry I can't recommened anything for the input provided";
            //String jsonData ="{\"recommendation\":\"" + recommendation + "\",\"uuid\":\"" + uuid + "\"}";
            //System.out.println(jsonData);

            //kafkaMessageService.setMessageReceived(true);

        }

    }

}
