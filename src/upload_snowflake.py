
import os
from pathlib import Path
from getpass import getpass

import snowflake.connector
from dotenv import load_dotenv

# Carrega as configurações do arquivo .env
load_dotenv()

# Identifica o diretório raiz do projeto
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Caminho do arquivo Parquet
PARQUET_FILE = PROJECT_DIR / "data/raw/clientes.parquet"

# Internal Stage de destino
STAGE = "RETAIL_ANALYTICS.RAW.STG_CLIENTES_PARQUET"

# Valida se o arquivo existe antes de conectar
if not PARQUET_FILE.is_file():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {PARQUET_FILE}"
    )

# Solicita a senha da chave privada RSA
private_key_password = getpass(
    "Digite a senha da chave privada RSA: "
)

# Estabelece a conexão com o Snowflake
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

try:
    cursor = conn.cursor()

    try:
        # Envia o arquivo local ao Internal Stage
        # AUTO_COMPRESS=FALSE mantém o arquivo .parquet
        # OVERWRITE=FALSE evita substituir arquivo existente
        put_sql = (
            f"PUT 'file://{PARQUET_FILE.as_posix()}' "
            f"@{STAGE} "
            "AUTO_COMPRESS=FALSE "
            "OVERWRITE=FALSE"
        )

        cursor.execute(put_sql)

        # Exibe o resultado do upload
        for row in cursor.fetchall():
            print("Resultado PUT:", row)

        # Lista os arquivos armazenados no Stage
        cursor.execute(f"LIST @{STAGE}")

        print("\nArquivos encontrados no Stage:")

        for row in cursor.fetchall():
            print(row)

    finally:
        cursor.close()

finally:
    conn.close()
