package com.supermaarkt.inventory_service.repository.postgres;


import java.util.Collection;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.supermaarkt.inventory_service.entity.postgres.Inventory;
import com.supermaarkt.inventory_service.repository.postgres.projection.PriceStockView;

public interface InventoryRepository extends JpaRepository<Inventory, Long>{
    
    @Query(value = "SELECT i.product.price as price, i.stock as stock, i.product.barcode as barcode "+ 
    "FROM Inventory i " +
    "WHERE i.product.barcode IN :barcodes")
    public List<PriceStockView> getPriceAndStockByBarcodes(@Param("barcodes") Collection<String> barcodes);

    public List<Inventory> findAllByProductBarcodeIn(Collection<String> barcodes);
}    
