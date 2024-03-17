package com.nlea.icecream.weatherservice.domain;

//import dev.autometrics.bindings.Autometrics;
import io.micrometer.observation.annotation.Observed;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;

import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import org.json.JSONArray;
import org.json.JSONObject;

@Observed(name="WeatherFetchService")
@Component
public class WeatherFetcher {

    @Value("${weatherbit.api.key}")
    private String apiKey;

    //@Autometrics
    public String getWeatherCondition(Double longitude, Double latitude){

        String url = "https://api.weatherbit.io/v2.0/current?lat=" + latitude + "&lon=" + longitude + "&key=" + apiKey + "&include=minutely";
        System.out.println(url);

        HttpClient httpClient = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).GET().build();


        try{
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("Response Code: " + response.statusCode());
            System.out.println("Response Body: " + response.body());
            String body = response.body();

            JSONObject jsonObject = new JSONObject(body);

            // Extract the "data" array
            JSONArray dataArray = jsonObject.getJSONArray("data");

            // Get the first element from the "data" array
            JSONObject firstDataObject = dataArray.getJSONObject(0);

            // Extract the "weather" object
            JSONObject weatherObject = firstDataObject.getJSONObject("weather");

            // Extract the value of the "description" field
            String description = weatherObject.getString("description");

            return description;


        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

}
