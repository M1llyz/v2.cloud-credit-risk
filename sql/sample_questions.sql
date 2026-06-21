-- =====================================================
-- CREDIT RISK ANALYSIS QUERIES
-- Project: PROJECT_ID (deve ser substituído pelo nome real do projeto criado na GCP e que foi definido em .env e settings.py)
-- Dataset: DATASET_ID (deve ser substituído pelo nome real do dataset criado no BigQuery que foi definido em .env e settings.py)
-- View: NOME_DA_VIEW (deve ser substituído pelo nome real da view criada em create_bigquery_views.sql ou arquivo parquet armazenado na Cloud Storage, eu já deixei os exemplos que utilizei, mas se você alterou em algum momento, certifique-se de usar o nome correto aqui também)
-- =====================================================

-- =====================================================
-- 1. Distribution of customers by risk category
-- =====================================================

SELECT
    target_label,
    COUNT(*) AS total_customers
FROM `PROJECT_ID.DATASET_ID.german_credit_silver`
GROUP BY target_label
ORDER BY total_customers DESC;

-- =====================================================
-- 2. Average credit amount by risk category
-- =====================================================

SELECT
    target_label,
    ROUND(AVG(credit_amount), 2) AS avg_credit_amount
FROM `PROJECT_ID.DATASET_ID.german_credit_silver`
GROUP BY target_label
ORDER BY avg_credit_amount DESC;

-- =====================================================
-- 3. Credit risk by loan purpose
-- =====================================================

SELECT *
FROM `PROJECT_ID.DATASET_ID.vw_purpose_risk_summary`
ORDER BY total_customers DESC;

-- =====================================================
-- 4. Credit risk by age group
-- =====================================================

SELECT *
FROM `PROJECT_ID.DATASET_ID.vw_age_risk_summary`
ORDER BY faixa_etaria;

-- =====================================================
-- 5. Most common credit histories among bad customers
-- =====================================================

SELECT
    credit_history,
    COUNT(*) AS total_bad_customers
FROM `PROJECT_ID.DATASET_ID.german_credit_silver`
WHERE target_label = 'bad'
GROUP BY credit_history
ORDER BY total_bad_customers DESC;

-- =====================================================
-- 6. Top 10 highest credit amounts
-- =====================================================

SELECT
    age,
    purpose,
    credit_amount,
    target_label
FROM `PROJECT_ID.DATASET_ID.german_credit_silver`
ORDER BY credit_amount DESC
LIMIT 10;

-- =====================================================
-- 7. Average credit amount by purpose
-- =====================================================

SELECT
    purpose,
    ROUND(AVG(credit_amount), 2) AS avg_credit_amount
FROM `PROJECT_ID.DATASET_ID.german_credit_silver`
GROUP BY purpose
ORDER BY avg_credit_amount DESC;