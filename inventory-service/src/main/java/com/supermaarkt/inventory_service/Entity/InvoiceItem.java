package com.supermaarkt.inventory_service.entity;

import java.math.BigDecimal;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class InvoiceItem {

    private String barcode;
    private BigDecimal pricePerUnit;
    private BigDecimal quantity;
    private BigDecimal total;

    public InvoiceItem(String barcode, BigDecimal pricePerUnit, BigDecimal quantity){
        this.barcode = barcode;
        this.pricePerUnit = pricePerUnit;
        this.quantity = quantity;
        this.total = this.pricePerUnit.multiply(this.quantity); 
    }
}
