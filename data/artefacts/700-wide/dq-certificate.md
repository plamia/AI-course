# Data Quality Certificate

[PASS] 1. No null order_date, region, or product_category
[PASS] 2. total_revenue > 0 for all rows
[PASS] 3. order_count > 0 for all rows
[PASS] 4. No duplicate (order_date, region, product_category) combinations
[PASS] 5. No null order_date
[PASS] 6. returns_rate_pct between 0.0 and 100.0 inclusive
[PASS] 7. returned_orders <= total_orders
[PASS] 8. order_date range spans at least 30 days

RESULT: 8/8 checks passed.