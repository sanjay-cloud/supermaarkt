package com.supermaarkt.inventory_service.repository.mongo;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.supermaarkt.inventory_service.entity.mongo.Invoice;


public interface InvoiceRepository extends MongoRepository<Invoice, String> {
    
}
