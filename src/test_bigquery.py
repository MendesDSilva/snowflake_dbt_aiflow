from google.cloud import bigquery

# Projeto Google Cloud
PROJECT_ID = "snowflake-dbt-project"

# Criar cliente autenticado
client = bigquery.Client(project=PROJECT_ID)

# Consulta de teste
query = """
SELECT
    COUNT(*) AS total_clientes
FROM `snowflake-dbt-project.stg_snfk_project.clientes`
"""

# Executar consulta
query_job = client.query(query)

# Recuperar resultados
for row in query_job.result():
    print(f"Total de clientes: {row.total_clientes}")
