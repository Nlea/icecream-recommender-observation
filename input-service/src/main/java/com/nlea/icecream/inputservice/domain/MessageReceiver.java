package com.nlea.icecream.inputservice.domain;

import org.apache.kafka.common.protocol.types.Field;
import org.springframework.stereotype.Component;

@Component
public class MessageReceiver {
    private Boolean received = false;
    private String busniessKey;


    public String getBusniessKey() {
        return busniessKey;
    }

    public void setBusniessKey(String busniessKey) {
        this.busniessKey = busniessKey;
    }



    public Boolean getReceived() {
        return received;
    }

    public void setReceived(Boolean received) {
        this.received = received;
    }




}
