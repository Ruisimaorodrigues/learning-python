from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

def chamar_api():
    url = "https://api.github.com/users/torvalds/repos"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    repos = response.json()
    logger.info(f"Total de repos encontrados: {len(repos)}")
    for repo in repos[:3]:
        logger.info(f"Repo: {repo['name']} | Stars: {repo['stargazers_count']}")
    return len(repos)

def processar_resultado(**context):
    total = context['ti'].xcom_pull(task_ids='chamar_api')
    logger.info(f"Pipeline concluído. Processados {total} repos.")

with DAG(
    dag_id='dag_api',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    tags=['exemplo', 'api']
) as dag:

    task_api = PythonOperator(
        task_id='chamar_api',
        python_callable=chamar_api
    )

    task_processar = PythonOperator(
        task_id='processar_resultado',
        python_callable=processar_resultado
    )

    task_api >> task_processar