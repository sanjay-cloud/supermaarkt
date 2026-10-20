package com.supermaarkt.inventory_service.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.mongo.Invoice;

@Service
public class DummyPaymentGateway {
    
    @KafkaListener(topics = "payment-topic", groupId="supermaarkt-group")
    public void processPayment(Invoice invoice) throws InterruptedException{
        System.out.println("Payment received invoice: "+invoice.getInvoiceNo());
        Thread.sleep(2000);
        System.err.println("Payment Success "+invoice.getGrandTotal()+" paid");
    }
}
