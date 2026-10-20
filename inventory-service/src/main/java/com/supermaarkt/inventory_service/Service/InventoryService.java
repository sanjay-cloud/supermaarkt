package com.supermaarkt.inventory_service.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.mongo.Invoice;
import com.supermaarkt.inventory_service.entity.postgres.Inventory;
import com.supermaarkt.inventory_service.entity.postgres.InvoiceItem;
import com.supermaarkt.inventory_service.repository.postgres.InventoryRepository;
import com.supermaarkt.inventory_service.repository.postgres.projection.PriceStockView;

import jakarta.transaction.Transactional;

@Service
public class InventoryService {
    
    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private InvoiceService invoiceService;

    @Autowired
    private PaymentProducer paymentProducer;

    public Inventory findById(Long id){
        Optional<Inventory> item = inventoryRepository.findById(id);
        return item.get();
    }

    public Invoice getPriceAndStockByBarcodes(List<String> barcodes){
        Map<String, BigDecimal> barcodeMap = getBarcodes(barcodes);
        Set<String> barcodesSet = barcodeMap.keySet();
        List<PriceStockView> prices = inventoryRepository.getPriceAndStockByBarcodes(barcodesSet);
        Invoice invoice = calculateBill(barcodeMap, prices);
        invoiceService.storeInvoice(invoice);
        updateInventoryStock(barcodeMap);
        // paymentProducer.sendPaymentRequest(invoice);
        return invoice;
    }

    public Map<String, BigDecimal> getBarcodes(List<String> barcodes){
        Map<String, BigDecimal> barcodeMap = new HashMap<>();

      for(String barcode : barcodes) {
         barcodeMap.put(barcode, (BigDecimal)barcodeMap.getOrDefault(barcode, new BigDecimal(0)).add(new BigDecimal(1)));
      }

      return barcodeMap;
    }
    

    public Invoice calculateBill(Map<String, BigDecimal> barcodesMap, List<PriceStockView> prices){

        List<InvoiceItem> invoiceItems = new ArrayList<>();
        for(PriceStockView priceObject : prices){
            String barcode = priceObject.getBarcode();
            BigDecimal itemQuantity = barcodesMap.get(priceObject.getBarcode());
            BigDecimal pricePerQuantity = priceObject.getPrice();
            InvoiceItem item = new InvoiceItem(barcode, pricePerQuantity, itemQuantity);
            invoiceItems.add(item);
        }

        return new Invoice(invoiceItems, "cash" );
    }

    @Transactional
    public void updateInventoryStock(Map<String, BigDecimal> barcodesMap){
        List<Inventory> items = inventoryRepository.findAllByProductBarcodeIn(barcodesMap.keySet());
        for(Inventory item : items){
            item.setStock(item.getStock().subtract( barcodesMap.get(item.getProduct().getBarcode())));
        }
        inventoryRepository.saveAll(items);
    }
}
