
# ============================================================
# PROJETO: BIGQUERY → SNOWFLAKE
# OBJETIVO: Extração parametrizada para arquivos Parquet
# ============================================================

import argparse
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import bigquery


# ============================================================
# 1. CONFIGURAÇÕES
# ============================================================

# Projeto e dataset de origem no BigQuery
PROJECT_ID = "snowflake-dbt-project"
DATASET_ID = "stg_snfk_project"

# Tabelas permitidas para extração
TABLES = [
    "avaliacoes",
    "carrinho",
    "categorias",
    "itens_pedidos",
    "pagamentos",
    "pedidos",
    "produtos",
]

# Diretório raiz do projeto
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Diretório de saída dos arquivos Parquet
OUTPUT_DIR = PROJECT_DIR / "data" / "raw"


# ============================================================
# 2. ARGUMENTOS DO TERMINAL
# ============================================================

# Permite informar a tabela ao executar o script
parser = argparse.ArgumentParser(
    description="Extrair uma tabela do BigQuery para Parquet"
)

parser.add_argument(
    "table",
    choices=TABLES,
    help="Nome da tabela que será extraída"
)

args = parser.parse_args()

table_name = args.table


# ============================================================
# 3. CONEXÃO COM BIGQUERY
# ============================================================

# Utiliza as credenciais ADC configuradas no WSL
client = bigquery.Client(project=PROJECT_ID)

# Identificador completo da tabela
table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"


# ============================================================
# 4. EXTRAÇÃO
# ============================================================

# Consulta todos os campos da tabela selecionada
query = f"""
SELECT *
FROM `{table_id}`
"""

# Executa a consulta e recupera os registros
query_job = client.query(query)

# Converte o resultado para pandas
df = query_job.result().to_dataframe(
    create_bqstorage_client=False
)

# Evita gerar arquivos vazios nesta primeira versão
if df.empty:
    raise ValueError(
        f"A tabela {table_name} não possui registros."
    )


# ============================================================
# 5. GERAÇÃO DO PARQUET
# ============================================================

# Cria o diretório caso não exista
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Define o caminho do arquivo
output_file = OUTPUT_DIR / f"{table_name}.parquet"

# Converte pandas para Arrow
arrow_table = pa.Table.from_pandas(
    df,
    preserve_index=False
)

# Grava o arquivo Parquet com compressão Snappy
pq.write_table(
    arrow_table,
    output_file,
    compression="snappy"
)


# ============================================================
# 6. VALIDAÇÃO E LOG
# ============================================================

# Lê os metadados do arquivo gerado
metadata = pq.read_metadata(output_file)

# Verifica se o arquivo contém a quantidade esperada
if metadata.num_rows != len(df):
    raise ValueError(
        "Quantidade de registros divergente no Parquet."
    )

print(f"Tabela: {table_name}")
print(f"Registros extraídos: {len(df)}")
print(f"Arquivo: {output_file}")
print(f"Tamanho: {output_file.stat().st_size:,} bytes")
print(f"Schema:\n{arrow_table.schema}")
