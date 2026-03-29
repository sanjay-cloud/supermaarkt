package com.supermaarkt.inventory_service.Controller;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.supermaarkt.inventory_service.Entity.Vendor;
import com.supermaarkt.inventory_service.Service.VendorService;

@Controller
@RequestMapping("/vendors")
public class VendorController {
    
    @Autowired
    private VendorService vendorService;

    @GetMapping(path="/{id}", produces=MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Vendor hello(@PathVariable(value="id") Long id){
        return vendorService.findById(id);
    }
}
