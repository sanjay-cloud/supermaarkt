package com.supermaarkt.inventory_service.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.supermaarkt.inventory_service.entity.Inventory;
import com.supermaarkt.inventory_service.entity.Invoice;
import com.supermaarkt.inventory_service.service.InventoryService;

@RestController
@RequestMapping("/inventory")
public class InventoryController {
    
    @Autowired
    private InventoryService inventoryService;

    @GetMapping(path = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Inventory getItem(@PathVariable(value = "id") Long id){
        return inventoryService.findById(id);
    }

    @PostMapping(path = "/billInvoice", produces = MediaType.APPLICATION_JSON_VALUE)
    public Invoice billInvoice(@RequestBody List<String> barcodes){
        return inventoryService.getPriceAndStockByBarcodes(barcodes);
    }
}
