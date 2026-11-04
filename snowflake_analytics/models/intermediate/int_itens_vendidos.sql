{{
    config(
        materialized='view',
        tags=['vendas']
    )
}}

WITH categorias AS (
    SELECT *
    FROM {{ ref('stg_categorias') }}
),

itens_pedidos AS (
    SELECT *
    FROM {{ ref('stg_itens_pedidos') }}
),

produtos AS (
    SELECT *
    FROM {{ ref('stg_produtos') }}
),

int_itens_vendidos AS (

    SELECT
        ip.PEDIDO_ID,
        ip.PRODUTO_ID,
        p.NOME AS NOME_PRODUTO,
        c.NOME AS NOME_CATEGORIA,
        ip.QUANTIDADE,
        ip.PRECO_UNITARIO,
        ip.SUBTOTAL

    FROM itens_pedidos ip

    LEFT JOIN produtos p
        ON ip.PRODUTO_ID = p.ID

    LEFT JOIN categorias c
        ON p.CATEGORIA_ID = c.ID

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'PRODUTO_ID',
            'NOME_PRODUTO',
            'NOME_CATEGORIA',
            'QUANTIDADE',
            'PRECO_UNITARIO',
            'SUBTOTAL'
        ]) }} AS ROW_HASH

    FROM int_itens_vendidos

)

SELECT *
FROM FINAL