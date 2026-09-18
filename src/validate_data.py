# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 19:00:41 2026

@author: bbrave
"""

import pandas as pd
from sqlalchemy import create_engine, text

from config import DATABASE_URL


QUERIES = {
    "total_orders": """
        SELECT COUNT(*) AS total_orders
        FROM analytics.fct_logistics_orders;
    """,

    "duplicate_orders": """
        SELECT COUNT(*) AS duplicated_orders
        FROM (
            SELECT order_id
            FROM analytics.fct_logistics_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) duplicated;
    """,

    "negative_values": """
        SELECT COUNT(*) AS negative_values
        FROM analytics.fct_logistics_orders
        WHERE order_value < 0
           OR freight_value < 0;
    """,

    "invalid_delivery_dates": """
        SELECT COUNT(*) AS invalid_dates
        FROM analytics.fct_logistics_orders
        WHERE order_delivered_customer_date IS NOT NULL
          AND order_purchase_timestamp
              > order_delivered_customer_date;
    """,

    "late_rate": """
        SELECT
            ROUND(
                100.0 * SUM(is_late)
                / NULLIF(SUM(is_delivered), 0),
                2
            ) AS late_rate_percentage
        FROM analytics.fct_logistics_orders;
    """
}


def run_quality_checks():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        for check_name, query in QUERIES.items():
            result = pd.read_sql(
                text(query),
                connection
            )

            print(f"\n{check_name}")
            print(result.to_string(index=False))


if __name__ == "__main__":
    run_quality_checks()