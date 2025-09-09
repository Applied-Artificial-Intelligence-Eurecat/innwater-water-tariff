WITH calculs AS (
    SELECT 
        id_projet,
        type_tarif,
        indice,
        bornes,
        prix_ht_op,
        LAG(prix_ht_op, 1, 0) OVER (PARTITION BY id_projet, type_tarif ORDER BY indice) AS prix_ht_op_precedent,
        CASE 
            WHEN indice = 0 THEN 0.0
            ELSE (prix_ht_op - LAG(prix_ht_op, 1, 0) OVER (PARTITION BY id_projet, type_tarif ORDER BY indice)) * CAST(bornes AS REAL)
        END AS calcul_unitaire
    FROM comon_tarif
)
SELECT 
    id_projet,
    type_tarif,
    indice,
    bornes,
    prix_ht_op,
    prix_ht_op_precedent,
    calcul_unitaire,
    SUM(calcul_unitaire) OVER (PARTITION BY id_projet, type_tarif ORDER BY indice ROWS UNBOUNDED PRECEDING) AS valeur_cumulative
FROM calculs
ORDER BY id_projet, type_tarif, indice;