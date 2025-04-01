
SELECT 
    o.Razao_Social, 
    b.reg_ans, 
    SUM(NULLIF(TRIM(REPLACE(b.vl_saldo_final, ',', '.')), '')::NUMERIC) AS total_despesas
FROM balanco_contabil b
JOIN operadoras o ON b.reg_ans = o.Registro_ANS
WHERE b.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
AND b.data >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY o.Razao_Social, b.reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

SELECT 
    o.Razao_Social, 
    b.reg_ans, 
    SUM(CAST(REPLACE(TRIM(b.vl_saldo_final), ',', '.') AS NUMERIC)) AS total_despesas
FROM balanco_contabil b
JOIN operadoras o ON b.reg_ans = o.Registro_ANS
WHERE b.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
AND b.data >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY o.Razao_Social, b.reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

WITH ultima_data AS (
    SELECT MAX(data) AS data_mais_recente FROM balanco_contabil
)
SELECT 
    o.Razao_Social, 
    b.reg_ans, 
    SUM(CAST(REPLACE(TRIM(b.vl_saldo_final), ',', '.') AS NUMERIC)) AS total_despesas
FROM balanco_contabil b
JOIN operadoras o ON b.reg_ans = o.Registro_ANS
JOIN ultima_data u ON b.data BETWEEN u.data_mais_recente - INTERVAL '3 months' AND u.data_mais_recente
WHERE b.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY o.Razao_Social, b.reg_ans
ORDER BY total_despesas DESC
LIMIT 10;

