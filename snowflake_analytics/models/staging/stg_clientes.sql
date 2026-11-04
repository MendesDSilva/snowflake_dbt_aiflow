WITH SOURCE AS (
    SELECT
        CAST(ID AS NUMBER(38,0)) AS ID
        ,LOWER(TRIM(NOME)) AS NOME
        ,LOWER(TRIM(EMAIL)) AS EMAIL
        ,REGEXP_REPLACE(TRIM(TELEFONE), '[^0-9]', '') AS TELEFONE
        ,cast(DATA_REGISTRO AS date) AS DATA_REGISTRO
        

    FROM {{ source('raw', 'CLIENTES') }}
),

FINAL AS (

    SELECT
        *,
        {{ row_hash(['NOME', 'EMAIL', 'TELEFONE']) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT * FROM FINAL