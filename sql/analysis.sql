DROP VIEW IF EXISTS v_project_kpis;
DROP VIEW IF EXISTS v_funnel_stages;
DROP VIEW IF EXISTS v_channel_performance;
DROP VIEW IF EXISTS v_campaign_performance;
DROP VIEW IF EXISTS v_monthly_performance;
DROP VIEW IF EXISTS v_device_user_performance;
DROP VIEW IF EXISTS v_region_performance;

CREATE VIEW v_project_kpis AS
SELECT
    COUNT(*) AS sessions,
    SUM(viewed_product_flag) AS product_views,
    SUM(added_to_cart_flag) AS carts,
    SUM(checkout_started_flag) AS checkouts,
    SUM(purchase_completed_flag) AS purchases,
    ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct,
    ROUND(SUM(revenue), 2) AS revenue
FROM ecommerce_sessions;

CREATE VIEW v_funnel_stages AS
WITH stages AS (
    SELECT 1 AS stage_order, 'Visited website' AS stage, SUM(visited_website_flag) AS sessions FROM ecommerce_sessions
    UNION ALL SELECT 2, 'Viewed product', SUM(viewed_product_flag) FROM ecommerce_sessions
    UNION ALL SELECT 3, 'Added to cart', SUM(added_to_cart_flag) FROM ecommerce_sessions
    UNION ALL SELECT 4, 'Checkout started', SUM(checkout_started_flag) FROM ecommerce_sessions
    UNION ALL SELECT 5, 'Purchase completed', SUM(purchase_completed_flag) FROM ecommerce_sessions
),
progression AS (
    SELECT
        stage_order,
        stage,
        sessions,
        LAG(sessions) OVER (ORDER BY stage_order) AS previous_stage_sessions,
        FIRST_VALUE(sessions) OVER (ORDER BY stage_order) AS total_sessions
    FROM stages
)
SELECT
    stage_order,
    stage,
    sessions,
    previous_stage_sessions,
    CASE
        WHEN previous_stage_sessions IS NULL THEN NULL
        ELSE previous_stage_sessions - sessions
    END AS drop_off_sessions,
    CASE
        WHEN previous_stage_sessions IS NULL THEN 100.0
        ELSE ROUND(100.0 * sessions / previous_stage_sessions, 2)
    END AS stage_conversion_rate_pct,
    ROUND(100.0 * sessions / total_sessions, 2) AS overall_conversion_rate_pct
FROM progression;

CREATE VIEW v_channel_performance AS
SELECT channel, COUNT(*) AS sessions, SUM(purchase_completed_flag) AS purchases,
       ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(revenue) / COUNT(*), 2) AS revenue_per_session
FROM ecommerce_sessions GROUP BY channel;

CREATE VIEW v_campaign_performance AS
SELECT campaign_type, COUNT(*) AS sessions, SUM(purchase_completed_flag) AS purchases,
       ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct,
       ROUND(SUM(revenue), 2) AS revenue
FROM ecommerce_sessions GROUP BY campaign_type;

CREATE VIEW v_monthly_performance AS
SELECT month, COUNT(*) AS sessions, SUM(purchase_completed_flag) AS purchases,
       ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct,
       ROUND(SUM(revenue), 2) AS revenue
FROM ecommerce_sessions GROUP BY month;

CREATE VIEW v_device_user_performance AS
SELECT device, user_type, COUNT(*) AS sessions, SUM(purchase_completed_flag) AS purchases,
       ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct
FROM ecommerce_sessions GROUP BY device, user_type;

CREATE VIEW v_region_performance AS
SELECT region, COUNT(*) AS sessions, SUM(purchase_completed_flag) AS purchases,
       ROUND(100.0 * SUM(purchase_completed_flag) / COUNT(*), 2) AS purchase_rate_pct,
       ROUND(SUM(revenue), 2) AS revenue
FROM ecommerce_sessions GROUP BY region;

