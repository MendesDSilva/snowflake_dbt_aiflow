{{
    config(
        materialized='view',
        tags=['vendas']
    )
}}

WITH clientes AS (
    SELECT *
    FROM {{ ref('stg_clientes') }}
),

pagamentos AS (
    SELECT *
    FROM {{ ref('stg_pagamentos') }}
),

pedidos AS (
    SELECT *
    FROM {{ ref('stg_pedidos') }}
),

int_pedidos_vendidos AS (

    SELECT
        p.DATA_PEDIDO,
        p.ID AS ID_PEDIDO,
        p.CLIENTE_ID,
        c.NOME AS NOME_CLIENTE,
        c.EMAIL AS EMAIL_CLIENTE,
        p.STATUS AS PEDIDO_STATUS,
        pg.METODO AS METODO_PAGAMENTO,
        pg.VALOR AS VALOR_PAGAMENTO

    FROM pedidos p

    LEFT JOIN clientes c
        ON p.CLIENTE_ID = c.ID

    LEFT JOIN pagamentos pg
        ON p.ID = pg.PEDIDO_ID

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'DATA_PEDIDO',
            'CLIENTE_ID',
            'NOME_CLIENTE',
            'EMAIL_CLIENTE',
            'PEDIDO_STATUS',
            'METODO_PAGAMENTO',
            'VALOR_PAGAMENTO'
        ]) }} AS ROW_HASH

    FROM int_pedidos_vendidos

)

SELECT *
FROM FINAL