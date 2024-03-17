package com.nlea.icecream.inputservice.websocket;

import com.nlea.icecream.inputservice.domain.InputMessage;
import com.nlea.icecream.inputservice.domain.MessageReceiver;
import com.nlea.icecream.inputservice.domain.Recommendation;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import org.springframework.util.MimeType;
import org.springframework.web.util.HtmlUtils;

import java.util.UUID;

@Controller
public class InputController {

    private final KafkaTemplate<String, String> kafkaTemplate;

    private final MessageReceiver messageReceiver;
    private final MeterRegistry meterRegistry;


    private final Recommendation recommendation;

    public InputController(KafkaTemplate kafkaTemplate, MessageReceiver messageReceiver, Recommendation recommendation, MeterRegistry meterRegistry){
        this.recommendation =recommendation;
        this.kafkaTemplate =kafkaTemplate;
        this.messageReceiver =messageReceiver;
        this.meterRegistry=meterRegistry;
    }



    @MessageMapping("/hello")
    @SendTo("/topic/recommendation")
    public Recommendation recommendation(InputMessage message) throws Exception {


        UUID uuid = UUID.randomUUID();
        String businessKey = uuid.toString();

        UUID uuid2 = UUID.randomUUID();
        String messageKey = uuid2.toString();

        messageReceiver.setBusniessKey(businessKey);

        String user_payLoad = "{\"location\":\"" + message.getLocation() + "\",\"mood\":\"" + message.getMood() + "\",\"buisnesskey\":\"" + businessKey + "\",\"location\":\"" + message.getLocation() +
                "\",\"name\":\"" + message.getName() + "\",\"dietRestrictions\":\"" + message.getDiet() + "\"}";


        kafkaTemplate.send("icecream.recommender.input", messageKey, user_payLoad);

        Boolean inbox = messageReceiver.getReceived();
        System.out.println(inbox);

        while (Boolean.FALSE.equals(inbox)) {
            System.out.println("Message not received");
            Thread.sleep(5000);
            inbox = messageReceiver.getReceived();
            System.out.println(inbox);
        }

        System.out.println("Outside the loop");

        messageReceiver.setReceived(Boolean.FALSE);


        return new Recommendation(recommendation.getContent());
        //Thread.sleep(1000); // simulated delay
        //return new Recommendation("Hello, " + HtmlUtils.htmlEscape(message.getName()) + "!");
    }



}
