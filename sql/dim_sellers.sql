DROP TABLE IF EXISTS analytics.dim_sellers;

CREATE TABLE analytics.dim_sellers AS
SELECT
	seller_id,
	seller_zip_code_prefix,
	seller_city,
	seller_state
FROM staging.sellers
GROUP BY seller_id;