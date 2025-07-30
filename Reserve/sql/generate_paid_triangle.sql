SELECT
    DATE_TRUNC('month', accident_date) AS accident_month,
    development_month,
    SUM(payment_amount) AS incremental_paid
FROM cleaned_claims
GROUP BY 1, 2
ORDER BY 1, 2;
