-- =====================================================
-- CREDIT RISK ANALYTICS VIEWS
-- Project: PROJECT_ID (deve ser substituído pelo nome real do projeto criado na GCP que deve ser definido em .env e settings.py)
-- Dataset: DATASET_ID (deve ser substituído pelo nome real do dataset criado no BigQuery definido anteriormente em .env e settings.py)
-- =====================================================

-- =====================================================
-- ATENÇÃO: Esse arquivo deve ser executado manualmente no BigQuery pra criação das views que serão usadas para análises e visualizações no Data Studio (antigo Looker) posteriormente, além de servir como base para as consultas SQL de exemplo que disponibilizei em 'sample_questions.sql'. Preferi não criar um script Python pra isso pra aprender a mexer mais no BigQuery mesmo, mas se você quiser automatizar, fique à vontade! :)
-- =====================================================

-- Risk distribution
CREATE OR REPLACE VIEW
`PROJECT_ID.DATASET_ID.vw_credit_risk_summary`
AS
SELECT
    CASE target_label
        WHEN 'good' THEN 'Bom'
        WHEN 'bad' THEN 'Mau'
        ELSE target_label
    END AS perfil_cliente,
    total_customers,
    avg_credit_amount,
    avg_age,
    avg_duration_months
FROM
    `PROJECT_ID.DATASET_ID.credit_risk_summary`;


-- Risk by credit purpose
CREATE OR REPLACE VIEW
`PROJECT_ID.DATASET_ID.vw_purpose_risk_summary`
AS
SELECT
    CASE purpose
        WHEN 'A40' THEN 'Carro novo'
        WHEN 'car_new' THEN 'Carro novo'

        WHEN 'A41' THEN 'Carro usado'
        WHEN 'car_used' THEN 'Carro usado'

        WHEN 'A42' THEN 'Móveis/equipamentos'
        WHEN 'furniture_equipment' THEN 'Móveis/equipamentos'

        WHEN 'A43' THEN 'Rádio/TV'
        WHEN 'radio_tv' THEN 'Rádio/TV'

        WHEN 'A44' THEN 'Eletrodomésticos'
        WHEN 'domestic_appliances' THEN 'Eletrodomésticos'

        WHEN 'A45' THEN 'Reparos'
        WHEN 'repairs' THEN 'Reparos'

        WHEN 'A46' THEN 'Educação'
        WHEN 'education' THEN 'Educação'

        WHEN 'A47' THEN 'Férias'
        WHEN 'vacation' THEN 'Férias'

        WHEN 'A48' THEN 'Requalificação profissional'
        WHEN 'retraining' THEN 'Requalificação profissional'

        WHEN 'A49' THEN 'Negócios'
        WHEN 'business' THEN 'Negócios'

        WHEN 'A410' THEN 'Outros'
        WHEN 'others' THEN 'Outros'

        ELSE purpose
    END AS finalidade_credito,

    CASE target_label
        WHEN 'good' THEN 'Bom'
        WHEN 'bad' THEN 'Mau'
        ELSE target_label
    END AS perfil_cliente,

    total_customers,
    avg_credit_amount
FROM
    `PROJECT_ID.DATASET_ID.purpose_risk_summary`;


-- Risk by age group
CREATE OR REPLACE VIEW
`PROJECT_ID.DATASET_ID.vw_age_risk_summary`
AS
SELECT
    age_group AS faixa_etaria,

    CASE target_label
        WHEN 'good' THEN 'Bom'
        WHEN 'bad' THEN 'Mau'
        ELSE target_label
    END AS perfil_cliente,

    total_customers,
    avg_credit_amount
FROM
    `PROJECT_ID.DATASET_ID.age_risk_summary`;


-- Detailed analytical view
CREATE OR REPLACE VIEW
`PROJECT_ID.DATASET_ID.vw_credit_analysis`
AS
SELECT
    checking_account_status,
    credit_history,
    purpose,
    credit_amount,
    age,
    target_label
FROM
   `PROJECT_ID.DATASET_ID.german_credit_silver`;