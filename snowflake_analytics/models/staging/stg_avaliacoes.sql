
WITH SOURCE AS (

    SELECT
        CAST(CLIENTE_ID AS NUMBER(38,0)) AS CLIENTE_ID,
        CAST(PRODUTO_ID AS NUMBER(38,0)) AS PRODUTO_ID,
        CAST(NOTA AS NUMBER(38,0)) AS NOTA,
        LOWER(TRIM(COMENTARIO)) AS COMENTARIO,
        CAST(DATA_AVALIACAO AS DATE) AS DATA_AVALIACAO

    FROM {{ source('raw', 'AVALIACOES') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'NOTA',
            'COMENTARIO',
            'DATA_AVALIACAO'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
