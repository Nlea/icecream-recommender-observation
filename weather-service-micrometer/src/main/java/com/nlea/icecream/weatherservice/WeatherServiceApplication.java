package com.nlea.icecream.weatherservice;

//import dev.autometrics.bindings.EnableAutometrics;
//import dev.autometrics.bindings.EnableAutometrics;
import dev.autometrics.bindings.EnableAutometrics;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.stereotype.Component;


@SpringBootApplication
@ComponentScan(basePackages = "com.nlea")
@EnableAutometrics
public class WeatherServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherServiceApplication.class, args);
	}

/*	@Bean
	public OtlpGrpcSpanExporter otlpHttpSpanExporter(@Value("${tracing.url}") String url) {
		return OtlpGrpcSpanExporter.builder().setEndpoint(url).build();
	}*/



}
