import pandas as pd
import json
from datetime import date
from pathlib import Path



def load_invoice_items(json_path : str):
    with open(json_path, 'r', encoding="utf-8") as file:
        invoices = json.load(file)      
    invoice_items_df = pd.json_normalize(
        invoices,
        record_path="invoiceItems",
        meta=[
            ["_id", "$oid"],
            ["grandTotal", "$numberDecimal"],
            "paymentMethod",
            ["dateTime","$date"]
        ],
        sep=".",
        )
    return invoice_items_df

def prepare_invoice_items(invoice_items_df :pd.DataFrame):
    invoice_items_df = invoice_items_df.rename(
        columns={
            "pricePerUnit.$numberDecimal": "price_per_unit",
            "quantity.$numberDecimal": "quantity",
            "total.$numberDecimal": "item_total",
            "_id.$oid": "invoice_id",
            "grandTotal.$numberDecimal": "invoice_total",
            "paymentMethod": "payment_method",
            "dateTime.$date": "date_time",
        }
    )
    
    invoice_items_df["barcode"] = invoice_items_df["barcode"].astype(str)
    invoice_items_df["invoice_id"] = invoice_items_df["invoice_id"].astype(str)

    invoice_items_df["price_per_unit"] = pd.to_numeric(invoice_items_df["price_per_unit"]).astype("float")
    invoice_items_df["quantity"] = pd.to_numeric(invoice_items_df["quantity"]).astype("Int64")
    invoice_items_df["item_total"] = pd.to_numeric(invoice_items_df["item_total"]).astype("float")
    invoice_items_df["invoice_total"] = pd.to_numeric(invoice_items_df["invoice_total"]).astype("float")

    invoice_items_df["date_time"] = pd.to_datetime(invoice_items_df["date_time"], utc=True)
    
    return invoice_items_df

def load_sales_data(json_path : str):
    invoice_items_df = load_invoice_items(json_path)
    invoice_items_df = prepare_invoice_items(invoice_items_df)
    return invoice_items_df

def aggregate_daily_product_sales(invoice_items_df: pd.DataFrame):
    daily_product_sales = (
            invoice_items_df.assign(sale_date=invoice_items_df["date_time"].dt.date)
            .groupby(
                ["barcode", "sale_date"],
                as_index=False,
            )
            .agg(
                price_per_unit=("price_per_unit", "first"),
                units_sold=("quantity", "sum"),
                sales_revenue=("item_total", "sum"),
            )
        )
    
    return daily_product_sales

def filter_daily_product_sales(barcode : str, sale_date: date, daily_sales_df: pd.DataFrame):

    filtered_sales_df = daily_sales_df[(daily_sales_df["barcode"] == barcode) & (daily_sales_df["sale_date"]== sale_date)]
    day_sales_df = daily_sales_df[daily_sales_df["sale_date"]== sale_date]
    filtered_sales_df["daily_share"] = (filtered_sales_df["units_sold"]/day_sales_df["units_sold"].sum())*100
    return filtered_sales_df


def save_df(save_path: str, daily_sales_df: pd.DataFrame):
    daily_sales_df.to_csv(save_path, index=False)

if __name__=="__main__":
    invoice_items_df = load_sales_data(r"data/raw/invoices.json")
    daily_sales_df = aggregate_daily_product_sales(invoice_items_df)
    save_df(r"data/processed/daily_sales.csv", daily_sales_df)
    filtered_sales_df = filter_daily_product_sales("3313456", date(2026, 11, 18), daily_sales_df)
    save_df(r"data/processed/filtered_sales.csv", filtered_sales_df)
    print(filtered_sales_df)