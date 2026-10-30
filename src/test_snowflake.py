
import os
from getpass import getpass

import snowflake.connector
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Solicita a senha utilizada para proteger a chave RSA
# Os caracteres digitados não aparecem no terminal
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
    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    try:
        # Consulta o contexto da sessão
        cursor.execute("""
            SELECT
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA()
        """)

        # Recupera e exibe o resultado
        result = cursor.fetchone()

        print("Conexão realizada com sucesso!")
        print(result)

    finally:
        # Fecha o cursor
        cursor.close()

finally:
    # Encerra a conexão
    conn.close()
