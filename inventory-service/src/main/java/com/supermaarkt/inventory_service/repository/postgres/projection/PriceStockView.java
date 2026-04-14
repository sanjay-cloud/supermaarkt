package com.supermaarkt.inventory_service.repository.postgres.projection;

import java.math.BigDecimal;

public interface PriceStockView {
    BigDecimal getPrice();
    BigDecimal getStock();
    String getBarcode();
}
