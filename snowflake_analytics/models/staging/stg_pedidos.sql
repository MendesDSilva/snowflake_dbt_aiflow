
WITH SOURCE AS (

    SELECT
        CAST(ID AS NUMBER(38,0)) AS ID,
        CAST(CLIENTE_ID AS NUMBER(38,0)) AS CLIENTE_ID,
        CAST(ENDERECO_ID AS NUMBER(38,0)) AS ENDERECO_ID,
        CAST(DATA_PEDIDO AS DATE) AS DATA_PEDIDO,
        LOWER(TRIM(STATUS)) AS STATUS

    FROM {{ source('raw', 'PEDIDOS') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'CLIENTE_ID',
            'ENDERECO_ID',
            'DATA_PEDIDO',
            'STATUS'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
