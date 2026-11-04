
WITH SOURCE AS (

    SELECT
        CAST(CLIENTE_ID AS NUMBER(38,0)) AS CLIENTE_ID,
        CAST(PRODUTO_ID AS NUMBER(38,0)) AS PRODUTO_ID,
        CAST(QUANTIDADE AS NUMBER(38,0)) AS QUANTIDADE,
        CAST(DATA_ADICIONADO AS DATE) AS DATA_ADICIONADO

    FROM {{ source('raw', 'CARRINHO') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'CLIENTE_ID',
            'PRODUTO_ID',
            'QUANTIDADE',
            'DATA_ADICIONADO'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
