
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import bigquery

PROJECT_ID = "snowflake-dbt-project"
TABLE_ID = f"{PROJECT_ID}.stg_snfk_project.clientes"

# Diretório de saída
OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "clientes.parquet"

# Cliente BigQuery com autenticação ADC
client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT
    id,
    nome,
    email,
    telefone,
    data_registro
FROM `{TABLE_ID}`
"""

# Executar consulta
query_job = client.query(query)

# Converter resultados em DataFrame
df = query_job.result().to_dataframe(
    create_bqstorage_client=False
)

# Validar registros
if df.empty:
    raise ValueError("A consulta não retornou registros.")

if df["id"].isna().any():
    raise ValueError("Existem clientes com ID nulo.")

if df["id"].duplicated().any():
    raise ValueError("Existem IDs de clientes duplicados.")

# Converter para tabela Arrow
table = pa.Table.from_pandas(
    df,
    preserve_index=False
)

# Gravar Parquet com compressão Snappy
pq.write_table(
    table,
    OUTPUT_FILE,
    compression="snappy"
)

print(f"Registros extraídos: {len(df)}")
print(f"Arquivo gerado: {OUTPUT_FILE}")
print(f"Tamanho: {OUTPUT_FILE.stat().st_size:,} bytes")
print(f"Schema Parquet:\n{table.schema}")
