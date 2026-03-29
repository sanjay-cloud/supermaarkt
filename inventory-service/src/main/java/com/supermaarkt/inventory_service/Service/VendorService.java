package com.supermaarkt.inventory_service.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.supermaarkt.inventory_service.entity.Vendor;
import com.supermaarkt.inventory_service.repository.VendorRepository;

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
