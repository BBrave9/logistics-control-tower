DROP TABLE IF EXISTS analytics.fct_logistics_orders;

CREATE TABLE analytics.fct_logistics_orders AS

WITH order_items_agg AS (
    SELECT
        oi.order_id,
        SUM(oi.price) AS order_value,
        SUM(oi.freight_value) AS freight_value,
        COUNT(*) AS item_count,
        COUNT(DISTINCT oi.seller_id) AS seller_count
    FROM staging.order_items oi
    GROUP BY oi.order_id
),

product_by_order AS (
    SELECT
        oi.order_id,
        STRING_AGG(
            DISTINCT COALESCE(
                p.product_category_name,
                'unknown'
            ),
            ', '
        ) AS product_categories
    FROM staging.order_items oi
    LEFT JOIN staging.products p
        ON oi.product_id = p.product_id
    GROUP BY oi.order_id
),

seller_by_order AS (
    SELECT
        oi.order_id,
        MIN(oi.seller_id) AS seller_id
    FROM staging.order_items oi
    GROUP BY oi.order_id
),

review_by_order AS (
    SELECT
        order_id,
        AVG(review_score)::numeric(10, 2) AS review_score
    FROM staging.reviews
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,

    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    seller_by_order.seller_id,
    s.seller_city,
    s.seller_state,

    product_by_order.product_categories,

    o.order_status,

    o.order_purchase_timestamp::timestamp
        AS order_purchase_timestamp,

    o.order_approved_at::timestamp
        AS order_approved_at,

    o.order_delivered_carrier_date::timestamp
        AS order_delivered_carrier_date,

    o.order_delivered_customer_date::timestamp
        AS order_delivered_customer_date,

    o.order_estimated_delivery_date::timestamp
        AS order_estimated_delivery_date,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN EXTRACT(
            DAY FROM (
                o.order_delivered_customer_date::timestamp
                - o.order_purchase_timestamp::timestamp
            )
        )
    END AS delivery_days,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN EXTRACT(
            DAY FROM (
                o.order_delivered_customer_date::timestamp
                - o.order_estimated_delivery_date::timestamp
            )
        )
    END AS delivery_delay_days,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN 1
        ELSE 0
    END AS is_delivered,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_delivered_customer_date::timestamp
             > o.order_estimated_delivery_date::timestamp
        THEN 1
        ELSE 0
    END AS is_late,

    order_items_agg.order_value,
    order_items_agg.freight_value,
    order_items_agg.item_count,
    order_items_agg.seller_count,

    review_by_order.review_score

FROM staging.orders o

LEFT JOIN staging.customers c
    ON o.customer_id = c.customer_id

LEFT JOIN seller_by_order
    ON o.order_id = seller_by_order.order_id

LEFT JOIN staging.sellers s
    ON seller_by_order.seller_id = s.seller_id

LEFT JOIN product_by_order
    ON o.order_id = product_by_order.order_id

LEFT JOIN order_items_agg
    ON o.order_id = order_items_agg.order_id

LEFT JOIN review_by_order
    ON o.order_id = review_by_order.order_id;