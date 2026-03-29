package com.supermaarkt.inventory_service.Service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.Entity.Vendor;
import com.supermaarkt.inventory_service.Repository.VendorRepository;

@Service
public class VendorService {
    @Autowired
    private VendorRepository vendorRepository;

    public VendorService(VendorRepository vendorRepository){
        this.vendorRepository = vendorRepository;
    }

    public Vendor findById(Long id){
        Optional<Vendor> vendor = vendorRepository.findById(id);
        return vendor.get();
    }
}
