
WITH SOURCE AS (

    SELECT
        CAST(ID AS NUMBER(38,0)) AS ID,
        LOWER(TRIM(NOME)) AS NOME,
        LOWER(TRIM(DESCRICAO)) AS DESCRICAO,
        CAST(CATEGORIA_ID AS NUMBER(38,0)) AS CATEGORIA_ID,
        CAST(PRECO AS NUMBER(12,2)) AS PRECO,
        LOWER(TRIM(MARCA)) AS MARCA,
        CAST(ESTOQUE AS NUMBER(38,0)) AS ESTOQUE,
        CAST(DATA_CADASTRO AS DATE) AS DATA_CADASTRO

    FROM {{ source('raw', 'PRODUTOS') }}

),

FINAL AS (

    SELECT
        *,
        {{ row_hash([
            'NOME',
            'DESCRICAO',
            'CATEGORIA_ID',
            'PRECO',
            'MARCA',
            'ESTOQUE',
            'DATA_CADASTRO'
        ]) }} AS ROW_HASH,
        {{ audit_columns() }}

    FROM SOURCE

)

SELECT *
FROM FINAL
