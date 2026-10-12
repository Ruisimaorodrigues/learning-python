from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import requests

logger = logging.getLogger(__name__)

DBT_PROJECT_DIR = "/opt/airflow/dbt/olist_dbt"
DBT_PROFILES_DIR = "/opt/airflow/dbt"

default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

def extrair_dados():
    """Extrai repos do GitHub como simulação de extracção de dados."""
    url = "https://api.github.com/users/torvalds/repos"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    repos = response.json()
    logger.info(f"Extraídos {len(repos)} registos da fonte")
    return len(repos)

with DAG(
    dag_id='dag_dbt_pipeline',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    default_args=default_args,
    tags=['dbt', 'pipeline']
) as dag:

    task_extrair = PythonOperator(
        task_id='extrair_dados',
        python_callable=extrair_dados
    )

    task_dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --profiles-dir {DBT_PROFILES_DIR}',
    )

    task_dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --profiles-dir {DBT_PROFILES_DIR}',
    )

    task_extrair >> task_dbt_run >> task_dbt_test