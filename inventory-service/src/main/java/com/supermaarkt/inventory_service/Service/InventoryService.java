package com.supermaarkt.inventory_service.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.Inventory;
import com.supermaarkt.inventory_service.repository.InventoryRepository;

@Service
public class InventoryService {
    
    @Autowired
    private InventoryRepository inventoryRepository;

    public Inventory finById(Long id){
        Optional<Inventory> inventory = inventoryRepository.findById(id);
        return inventory.get();
    }
}
