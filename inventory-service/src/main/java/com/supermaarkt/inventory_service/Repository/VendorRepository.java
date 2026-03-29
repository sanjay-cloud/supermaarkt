package com.supermaarkt.inventory_service.repository;



import org.springframework.data.jpa.repository.JpaRepository;

import com.supermaarkt.inventory_service.entity.Vendor;

public interface VendorRepository extends JpaRepository<Vendor, Long> {
}
