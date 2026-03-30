package com.supermaarkt.inventory_service.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.Product;
import com.supermaarkt.inventory_service.repository.ProductRepository;

@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public ProductService(ProductRepository productRepository){
        this.productRepository = productRepository;
    }

    public Product findById(String id){
        Optional<Product> product = productRepository.findById(id);
        return product.get();
    }
}
