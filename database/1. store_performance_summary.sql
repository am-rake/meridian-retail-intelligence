-- Meridian Retail Intelligence
-- Store Performance Summary
-- Purpose: Calculate financial performance metrics
-- for all retail locations and the online sales channel.
-- Data source: Synthetic retail transactions

CREATE OR REPLACE VIEW public.store_performance_summary
WITH (security_invoker = true)
AS

SELECT
    s.store_id,
    s.store_name,

    COUNT(o.order_id) AS total_orders,

    COALESCE(
        ROUND(SUM(o.order_total_usd), 2),
        0
    ) AS total_revenue,

    COALESCE(
        ROUND(SUM(o.cost_of_goods_usd), 2),
        0
    ) AS total_cost,

    COALESCE(
        ROUND(SUM(o.gross_profit_usd), 2),
        0
    ) AS gross_profit,

    ROUND(
        SUM(o.gross_profit_usd) * 100.0 /
        NULLIF(SUM(o.order_total_usd), 0),
        2
    ) AS gross_margin_pct,

    ROUND(
        AVG(o.order_total_usd),
        2
    ) AS average_order_value

FROM public.stores s

LEFT JOIN public.orders o
    ON s.store_id = o.store_id

GROUP BY
    s.store_id,
    s.store_name;