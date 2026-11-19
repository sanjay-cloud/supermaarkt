from app.analytics.daily_metrics import aggregate_daily_product_sales
import pytest
import pandas as pd
from datetime import date

@pytest.fixture
def invoice_items_df():
    return pd.DataFrame(
    {
        "barcode": ["3313456", "3313456", "4313457"],
        "date_time": pd.to_datetime(
            [
                "2026-11-18T10:00:00Z",
                "2026-11-18T14:00:00Z",
                "2026-11-18T15:00:00Z",
            ]
        ),
        "price_per_unit": [1.0, 1.0, 2.0],
        "quantity": [2, 3, 4],
        "item_total": [2.0, 3.0, 8.0],
    }
)
@pytest.fixture
def daily_sales_df(invoice_items_df):
    return aggregate_daily_product_sales(invoice_items_df)

def test_daily_sales_preserves_quantity(invoice_items_df, daily_sales_df):
    assert (
        invoice_items_df["quantity"].sum()
        == daily_sales_df["units_sold"].sum()
    ), "Quantity changed during aggregation"


def test_filter_daily_product_sales(invoice_items_df, daily_sales_df):    
    assert(
            daily_sales_df["sales_revenue"].sum() == invoice_items_df["item_total"].sum()
        ),"revenues do not match"

def test_actual_grouping(daily_sales_df):
        expected_df = pd.DataFrame(
            {
                "barcode": ["3313456", "4313457"],
                "sale_date": [
                    date(2026, 11, 18),
                    date(2026, 11, 18),
                ],
                "price_per_unit": [1.0, 2.0],
                "units_sold": [5, 4],
                "sales_revenue": [5.0, 8.0],
            }
        )

        actual_df = (
            daily_sales_df
            .sort_values(["barcode", "sale_date"])
            .reset_index(drop=True)
        )

        expected_df = (
            expected_df
            .sort_values(["barcode", "sale_date"])
            .reset_index(drop=True)
        )

        pd.testing.assert_frame_equal(actual_df, expected_df)    