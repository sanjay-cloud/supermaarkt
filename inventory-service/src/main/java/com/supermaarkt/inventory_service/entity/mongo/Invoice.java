package com.supermaarkt.inventory_service.entity.mongo;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import com.supermaarkt.inventory_service.entity.postgres.InvoiceItem;

import lombok.Data;
import lombok.NoArgsConstructor;
@Document(collection = "invoices")
@Data
@NoArgsConstructor
public class Invoice {

    @Id
    private String invoiceNo;

    private List<InvoiceItem> invoiceItems;
    private BigDecimal grandTotal;
    private String paymentMethod;
    private LocalDateTime dateTime;

    public Invoice(List<InvoiceItem> invoiceItems, String paymentMethod){
        this.invoiceItems = invoiceItems;
        this.paymentMethod = paymentMethod;
        BigDecimal total = BigDecimal.ZERO;
        for(InvoiceItem item : invoiceItems){
            total = total.add(item.getTotal());
        }
        this.dateTime = LocalDateTime.now();

        this.grandTotal = total;
    }
}
