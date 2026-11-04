
WITH SOURCE AS (

    SELECT
        CAST(PEDIDO_ID AS NUMBER(38,0)) AS PEDIDO_ID,
        CAST(PRODUTO_ID AS NUMBER(38,0)) AS PRODUTO_ID,
        CAST(QUANTIDADE AS NUMBER(38,0)) AS QUANTIDADE,
        CAST(PRECO_UNITARIO AS NUMBER(12,2)) AS PRECO_UNITARIO,
        CAST(SUBTOTAL AS NUMBER(14,2)) AS SUBTOTAL

    FROM {{ source('raw', 'ITENS_PEDIDOS') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'QUANTIDADE',
            'PRECO_UNITARIO',
            'SUBTOTAL'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
