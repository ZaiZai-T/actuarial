-- Step 1: Drop existing cleaned table if exists
DROP TABLE IF EXISTS cleaned_claims;

-- Step 2: Create new cleaned_claims table with processed fields
CREATE TABLE cleaned_claims AS
SELECT
    claim_id,
    policy_id,
    accident_date::DATE,
    report_date::DATE,
    payment_date::DATE,
    development_month::INTEGER,
    ROUND(payment_amount::NUMERIC, 2) AS payment_amount,
    claim_status,
    claim_type,
    coverage_type,
    region,
    insured_age::INTEGER,
    vehicle_age::INTEGER,
    claim_channel,

    -- New derived fields
    (payment_date::DATE - accident_date::DATE) AS development_lag,
    (report_date::DATE - accident_date::DATE) AS report_lag,
    CASE
        WHEN claim_status ILIKE 'Closed' THEN TRUE
        ELSE FALSE
    END AS is_closed

FROM insurance_claims
WHERE
    claim_id IS NOT NULL
    AND accident_date IS NOT NULL
    AND report_date IS NOT NULL
    AND payment_amount IS NOT NULL
    AND payment_amount >= 0;

