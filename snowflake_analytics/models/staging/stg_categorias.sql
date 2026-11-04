WITH SOURCE AS (
    SELECT
        CAST(ID AS NUMBER(38,0)) AS ID
        ,LOWER(TRIM(NOME)) AS NOME
        

    FROM {{ source('raw', 'CATEGORIAS') }}
),

FINAL AS (

    SELECT
        *,
        {{ row_hash(['NOME']) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT * FROM FINAL

