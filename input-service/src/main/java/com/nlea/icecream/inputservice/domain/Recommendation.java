package com.nlea.icecream.inputservice.domain;

import org.springframework.stereotype.Component;

@Component
    public class Recommendation {
        private String content;

        public Recommendation( ){

        }

        public Recommendation(String content){
            this.content =content;
        }
        public void setContent(String content){
            this.content = content;

        }

        public String getContent(){
            return content;
        }
    }

