package com.supermaarkt.inventory_service.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.supermaarkt.inventory_service.entity.Inventory;

public interface InventoryRepository extends JpaRepository<Inventory, Long>{
    
}
