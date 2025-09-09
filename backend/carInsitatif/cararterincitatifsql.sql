SELECT 
    ROUND(AVG(water_consumption_ibt), 2) AS moyenne,
    ROUND(MIN(water_consumption_ibt), 2) AS minimum,
    ROUND(MAX(water_consumption_ibt), 2) AS maximum,
    COUNT(*) AS nombre_menages
FROM carInsitatifdataintermed;
/---------------------------Moyenne à max ----------------------------/

WITH ordered_data AS (
    SELECT 
        water_consumption_ibt,
        ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM carInsitatifdataintermed
),
median_calc AS (
    SELECT 
        AVG(water_consumption_ibt) AS median_value
    FROM ordered_data
    WHERE row_num IN (
        (total_count + 1) / 2,
        (total_count + 2) / 2
    )
)
SELECT 
    ROUND(AVG(c.water_consumption_ibt), 2) AS moyenne,
    ROUND(MIN(c.water_consumption_ibt), 2) AS minimum,
    ROUND(MAX(c.water_consumption_ibt), 2) AS maximum,
    COUNT(*) AS nombre_menages,
    ROUND(m.median_value, 2) AS mediane
FROM carInsitatifdataintermed c
CROSS JOIN median_calc m;


/--------------------------Q1----------------------------------------/

WITH ranked_data AS (
    SELECT 
        water_consumption_ibt,
        ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM carInsitatifdataintermed
)
SELECT 
    water_consumption_ibt AS percentile_25
FROM ranked_data
WHERE row_num = CEIL(0.25 * total_count);



/-----------------------Q3- OK------------------------------/

WITH ranked_data AS (
    SELECT 
        water_consumption_ibt,
        ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM carInsitatifdataintermed
)
SELECT 
    ROUND(water_consumption_ibt, 2) AS percentile_75
FROM ranked_data
WHERE row_num = CEIL(0.75 * total_count);


/---------------------D1---------------------------------/

WITH ranked_data AS (
    SELECT 
        water_consumption_ibt,
        ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM carInsitatifdataintermed
)
SELECT 
    water_consumption_ibt AS percentile_10
FROM ranked_data
WHERE row_num = CEIL(0.1 * total_count);

/-----------------D9----OK--------------/

WITH ranked_data AS (
    SELECT 
        water_consumption_ibt,
        ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM carInsitatifdataintermed
)
SELECT 
    water_consumption_ibt AS percentile_90
FROM ranked_data
WHERE row_num = CEIL(0.9 * total_count);

/-------------------F-------------------------/

WITH stats AS (
    SELECT 
        AVG(water_consumption_ibt) AS moyenne_consommation,
        COUNT(*) AS total_count
    FROM carInsitatifdataintermed
),
below_avg_count AS (
    SELECT 
        COUNT(*) AS count_below_avg
    FROM carInsitatifdataintermed
    WHERE water_consumption_ibt <= (SELECT moyenne_consommation FROM stats)
)
SELECT 
    ROUND(100.0 * count_below_avg / total_count, 2) AS rang_percentile_moyenne
FROM stats, below_avg_count;

/--------------------- ?------------------------------------------/
WITH filtered_data AS (
    WITH ranked_data AS (
        SELECT 
            water_consumption_ibt,
            ROW_NUMBER() OVER (ORDER BY water_consumption_ibt) AS row_num,
            COUNT(*) OVER () AS total_count
        FROM carInsitatifdataintermed
    )
    SELECT water_consumption_ibt
    FROM ranked_data
    WHERE row_num >= CEIL(0.9 * total_count)  -- Top 10%
    -- WHERE row_num <= CEIL(0.1 * total_count)  -- Bottom 10%
    -- WHERE row_num BETWEEN CEIL(0.25 * total_count) AND CEIL(0.75 * total_count)  -- Interquartile
)
SELECT 
    ROUND(SUM(POWER(water_consumption_ibt - moyenne, 2)) / (COUNT(*) - 1), 2) AS variance
FROM filtered_data
CROSS JOIN (
    SELECT AVG(water_consumption_ibt) AS moyenne 
    FROM filtered_data
) AS avg_calc;

/----------------------Variance--------------------------------/

SELECT 
    ROUND(SUM(POWER(water_consumption_ibt - moyenne, 2)) / (COUNT(*) - 1), 3) AS variance_echantillon
FROM carInsitatifdataintermed
CROSS JOIN (
    SELECT AVG(water_consumption_ibt) AS moyenne 
    FROM carInsitatifdataintermed
) AS avg_calc;


/----------------------------------Ecart-type------------------------------------------ /

SELECT 
    ROUND(SQRT(SUM(POWER(water_consumption_ibt - moyenne, 2)) / (COUNT(*) - 1)), 3) AS ecart_type_echantillon
FROM carInsitatifdataintermed
CROSS JOIN (
    SELECT AVG(water_consumption_ibt) AS moyenne 
    FROM carInsitatifdataintermed
) AS avg_calc;

