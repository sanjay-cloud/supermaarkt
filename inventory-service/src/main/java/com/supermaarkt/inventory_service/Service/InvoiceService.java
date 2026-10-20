package com.supermaarkt.inventory_service.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.mongo.Invoice;
import com.supermaarkt.inventory_service.repository.mongo.InvoiceRepository;

@Service
public class InvoiceService {

    @Autowired
    private InvoiceRepository invoiceRepository;

    public void storeInvoice(Invoice invoice){
        invoiceRepository.save(invoice);
    }
}
