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

produtos AS (
    SELECT *
    FROM {{ ref('stg_produtos') }}
),

avaliacoes AS (
    SELECT *
    FROM {{ ref('stg_avaliacoes') }}
),

int_avaliacoes_vendas AS (

    SELECT
        a.DATA_AVALIACAO,
        a.CLIENTE_ID,
        c.NOME AS NOME_CLIENTE,
        a.PRODUTO_ID,
        p.NOME AS NOME_PRODUTO,
        a.NOTA,
        a.COMENTARIO

    FROM avaliacoes a

    LEFT JOIN clientes c
        ON a.CLIENTE_ID = c.ID

    LEFT JOIN produtos p
        ON a.PRODUTO_ID = p.ID

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'DATA_AVALIACAO',
            'CLIENTE_ID',
            'NOME_CLIENTE',
            'PRODUTO_ID',
            'NOME_PRODUTO',
            'NOTA',
            'COMENTARIO'
        ]) }} AS ROW_HASH

    FROM int_avaliacoes_vendas

)

SELECT *
FROM FINAL