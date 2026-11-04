
WITH SOURCE AS (

    SELECT
        CAST(ID AS NUMBER(38,0)) AS ID,
        CAST(PEDIDO_ID AS NUMBER(38,0)) AS PEDIDO_ID,
        CAST(VALOR AS NUMBER(12,2)) AS VALOR,
        TRIM(METODO) AS METODO,
        LOWER(TRIM(STATUS)) AS STATUS,
        CAST(DATA_PAGAMENTO AS DATE) AS DATA_PAGAMENTO

    FROM {{ source('raw', 'PAGAMENTOS') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'PEDIDO_ID',
            'VALOR',
            'METODO',
            'STATUS',
            'DATA_PAGAMENTO'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
