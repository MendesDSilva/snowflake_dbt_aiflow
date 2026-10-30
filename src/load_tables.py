
# ============================================================
# PROJETO: BIGQUERY → SNOWFLAKE
# OBJETIVO: Upload e carga parametrizada de arquivos Parquet
# ============================================================

import argparse
import os
from getpass import getpass
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


# ============================================================
# 1. CONFIGURAÇÕES
# ============================================================

load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Tabelas permitidas para carga
TABLES = [
    "avaliacoes",
    "carrinho",
    "categorias",
    "itens_pedidos",
    "pagamentos",
    "pedidos",
    "produtos",
]

# Stage compartilhado
STAGE = "RETAIL_ANALYTICS.RAW.STG_INGESTAO"

# Formato Parquet cadastrado no Snowflake
FILE_FORMAT = "RETAIL_ANALYTICS.RAW.FF_PARQUET"


# ============================================================
# 2. ARGUMENTOS
# ============================================================

parser = argparse.ArgumentParser(
    description="Carregar Parquet no Snowflake"
)

parser.add_argument(
    "table",
    choices=TABLES,
    help="Tabela que será carregada"
)

args = parser.parse_args()

table_name = args.table

# Caminho do Parquet local
parquet_file = PROJECT_DIR / "data" / "raw" / f"{table_name}.parquet"

if not parquet_file.is_file():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {parquet_file}"
    )


# ============================================================
# 3. AUTENTICAÇÃO RSA
# ============================================================

private_key_password = getpass(
    "Digite a senha da chave privada RSA: "
)

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    authenticator=os.getenv("SNOWFLAKE_AUTHENTICATOR"),
    private_key_file=os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH"),
    private_key_file_pwd=private_key_password,
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)


# ============================================================
# 4. UPLOAD PARA O STAGE
# ============================================================

try:
    cursor = conn.cursor()

    try:
        stage_path = f"@{STAGE}/{table_name}/"

        put_sql = (
            f"PUT 'file://{parquet_file.as_posix()}' "
            f"{stage_path} "
            "AUTO_COMPRESS=FALSE "
            "OVERWRITE=TRUE"
        )

        cursor.execute(put_sql)

        print("\nResultado do PUT:")

        for row in cursor.fetchall():
            print(row)


        # ====================================================
        # 5. COPY INTO
        # ====================================================

        target_table = f"RETAIL_ANALYTICS.RAW.{table_name.upper()}"

        copy_sql = f"""
        COPY INTO {target_table}
        FROM {stage_path}
        FILE_FORMAT = (
            FORMAT_NAME = '{FILE_FORMAT}'
        )
        MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
        ON_ERROR = ABORT_STATEMENT
        """

        cursor.execute(copy_sql)

        print("\nResultado do COPY INTO:")

        for row in cursor.fetchall():
            print(row)


        # ====================================================
        # 6. VALIDAÇÃO
        # ====================================================

        cursor.execute(
            f"SELECT COUNT(*) FROM {target_table}"
        )

        total = cursor.fetchone()[0]

        print(f"\nTabela: {target_table}")
        print(f"Total de registros: {total}")

    finally:
        cursor.close()

finally:
    conn.close()
