package  com.supermaarkt.inventory_service.entity;

import java.time.LocalDateTime;

import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Table(name = "Products")
@Data
@EntityListeners(AuditingEntityListener.class)
public class Product{

    @Id
    private String barcode;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private int price;

    @Column(name = "shelf_life")
    private Integer ShelfLife;

    @ManyToOne
    @JoinColumn(name="category_id")
    private ProductCategory category;

    @ManyToOne
    @JoinColumn(name="vendor_id")
    private Vendor vendor;

    @CreatedBy
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedBy
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
}