# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:25:00 2026

@author: bbrave
"""

import pandas as pd

from config import RAW_DATA_DIR


def load_orders():
    """Carrega o arquivo de pedidos."""
    file_path = RAW_DATA_DIR / "olist_orders_dataset.csv"

    orders = pd.read_csv(file_path)

    return orders


def inspect_orders(orders):
    """Exibe informações básicas sobre os pedidos."""
    print("Dimensões:", orders.shape)
    print("\nColunas:")
    print(orders.columns.tolist())

    print("\nTipos de dados:")
    print(orders.dtypes)

    print("\nValores nulos:")
    print(orders.isna().sum())

    print("\nStatus dos pedidos:")
    print(orders["order_status"].value_counts(dropna=False))


if __name__ == "_main_":
    orders_df = load_orders()
    inspect_orders(orders_df)