package com.supermaarkt.inventory_service.repository.postgres;



import org.springframework.data.jpa.repository.JpaRepository;

import com.supermaarkt.inventory_service.entity.postgres.Vendor;

public interface VendorRepository extends JpaRepository<Vendor, Long> {
}
