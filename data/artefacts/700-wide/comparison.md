# AI Agent Pipeline Comparison

### 1. One Time-Saving Success
The agent successfully generated 500 rows of synthetic data with exact distributions (4% nulls, 2% duplicates) and perfectly handled the complex Silver layer cleaning. It correctly wrote the `TRY_STRPTIME` logic to parse the three different mixed date formats and deduplicated the rows in seconds. Writing that boilerplate DuckDB SQL by hand would have taken 10+ minutes.

### 2. One Mistake Caught by Human Review
**Business Logic Error in Gold Layer:** The agent calculated the `dropout_rate_pct` incorrectly. It divided the `dropped_count` by only the `completed` and `dropped` students, completely ignoring the `in_progress` students in the denominator. A human reviewer caught this because the denominator must reflect `total_enrollments` to give an accurate percentage. I fixed this by changing the denominator to `COUNT(event_id)`.
