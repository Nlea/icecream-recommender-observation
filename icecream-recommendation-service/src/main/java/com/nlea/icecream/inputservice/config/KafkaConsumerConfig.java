package com.nlea.icecream.inputservice.config;

import io.micrometer.core.instrument.MeterRegistry;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.ssl.SslBundles;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.core.MicrometerConsumerListener;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaConsumerConfig {

    @Value(value = "${spring.kafka.bootstrap-servers}")
    private String bootstrapAddress;

    private final KafkaProperties kafkaProperties;
    private final MeterRegistry meterRegistry;
    @Autowired
    public KafkaConsumerConfig(KafkaProperties kafkaProperties, MeterRegistry meterRegistry) {
        this.kafkaProperties = kafkaProperties;
        this.meterRegistry = meterRegistry;
    }

    @SuppressWarnings("resource")
    @Bean
    public Map<String, Object> consumerConfigs(SslBundles sslBundles) {
        Map<String, Object> props = new HashMap<>();
        props.put(
                ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,
                bootstrapAddress);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "groupID");
        props.put(
                ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
                Serdes.String().deserializer().getClass().getName());
        props.put(
                ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
                Serdes.String().deserializer().getClass().getName());
        return props;
    }

    @Bean
    public ConsumerFactory<String, String> consumerFactory(SslBundles sslBundles) {
        ConsumerFactory<String, String> factory = new DefaultKafkaConsumerFactory<>(consumerConfigs(sslBundles));
        factory.addListener(new MicrometerConsumerListener<>(meterRegistry));
        return factory;
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory(SslBundles sslBundles) {
        ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.getContainerProperties().setObservationEnabled(true);
        factory.getContainerProperties().setGroupId("icecream-group");
        factory.setConsumerFactory(consumerFactory(sslBundles));
        factory.setMissingTopicsFatal(false);
        return factory;
    }

}