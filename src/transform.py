# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:38:16 2026

@author: bbrave
"""

import pandas as pd


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def convert_date_columns(df):
    """
    Converte as colunas de data para datetime.
    """
    df = df.copy()

    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


def calculate_delivery_metrics(df):
    """
    Calcula métricas básicas de entrega.
    """
    df = df.copy()

    df["is_delivered"] = (
        df["order_delivered_customer_date"].notna()
    ).astype(int)

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.days

    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.days

    df["is_late"] = (
        (
            df["order_delivered_customer_date"]
            > df["order_estimated_delivery_date"]
        )
        & df["order_delivered_customer_date"].notna()
    ).astype(int)

    return df