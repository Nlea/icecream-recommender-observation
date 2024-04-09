package com.nlea.icecream.inputservice.domain;

import org.springframework.stereotype.Component;


public class InputMessage {
    private String name;

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getMood() {
        return mood;
    }

    public void setMood(String mood) {
        this.mood = mood;
    }

    public String getDiet() {
        return diet;
    }

    public void setDiet(String diet) {
        this.diet = diet;
    }

    private String location;
    private String mood;
    private String diet;

    public InputMessage(){

    }

    public InputMessage(String name){

    }

    public void setName(String name){
        this.name =name;

    }
    public String getName(){
        return name;
    }
}

