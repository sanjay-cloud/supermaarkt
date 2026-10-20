package com.supermaarkt.inventory_service.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.mongo.Invoice;

@Service
public class PaymentProducer {
    @Autowired
    private KafkaTemplate<String, Invoice> kafkaTemplate;
    
    public void sendPaymentRequest(Invoice invoice){
        kafkaTemplate.send("payment-topic", invoice);
    }
}
