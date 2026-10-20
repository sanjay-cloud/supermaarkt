package com.supermaarkt.inventory_service.repository.postgres;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.supermaarkt.inventory_service.entity.postgres.Product;

public interface ProductRepository extends JpaRepository<Product, String>{
    
    public List<String> findByBarcodeIn(List<String> barcodes);
}
