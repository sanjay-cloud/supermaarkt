from datetime import date
from fastapi import APIRouter
from app.analytics.daily_metrics import filter_daily_product_sales
import pandas as pd
router = APIRouter()


@router.get("/analytics/daily-sales")
def get_daily_sales(sale_date : date, barcode: str):
    daily_sales_df = pd.read_csv("data/processed/daily_sales.csv",dtype={"barcode": str})
    daily_sales_df["sale_date"] = pd.to_datetime(daily_sales_df["sale_date"], utc=True).dt.date
    return filter_daily_product_sales(barcode=barcode, sale_date=sale_date, daily_sales_df=daily_sales_df).to_dict(orient="records")