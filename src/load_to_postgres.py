# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:47:47 2026

@author: bbrave
"""

import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, RAW_DATA_DIR


FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
}


def create_database_engine():
    """
    Cria conexão com o PostgreSQL.
    """
    return create_engine(DATABASE_URL)


def load_csv_to_postgres(engine, table_name, file_name):
    """
    Carrega um CSV para a camada staging.
    """
    file_path = RAW_DATA_DIR / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    print(
        f"Tabela staging.{table_name} carregada "
        f"com {len(df)} registros."
    )


def main():
    engine = create_database_engine()

    for table_name, file_name in FILES.items():
        load_csv_to_postgres(
            engine=engine,
            table_name=table_name,
            file_name=file_name,
        )


if __name__ == "__main__":
    main()