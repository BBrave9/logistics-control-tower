DROP TABLE IF EXISTS analytics.dim_geolocation;

CREATE TABLE analytics.dim_geolocation AS
SELECT
    geolocation_zip_code_prefix,
    AVG(geolocation_lat) AS latitude,
    AVG(geolocation_lng) AS longitude,
    MAX(geolocation_city) AS city,
    MAX(geolocation_state) AS state
FROM staging.geolocation
GROUP BY geolocation_zip_code_prefix;