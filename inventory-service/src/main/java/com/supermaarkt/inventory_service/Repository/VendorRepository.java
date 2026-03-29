package com.supermaarkt.inventory_service.Repository;



import org.springframework.data.jpa.repository.JpaRepository;

import com.supermaarkt.inventory_service.Entity.Vendor;

public interface VendorRepository extends JpaRepository<Vendor, Long> {
}
