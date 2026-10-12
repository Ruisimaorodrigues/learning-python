from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import requests

logger = logging.getLogger(__name__)

def extrair_com_checkpoint(**context):
    """
    Extracção com checkpoint — se falhar a meio, recomeça do ponto de falha.
    Usa XCom para guardar o progresso.
    """
    # Simula extracção paginada com checkpoint
    paginas_processadas = context['ti'].xcom_pull(
        task_ids='extrair_com_checkpoint', 
        key='paginas_processadas'
    ) or 0
    
    logger.info(f"A recomeçar do checkpoint: página {paginas_processadas}")
    
    total_repos = []
    for page in range(paginas_processadas + 1, 4):
        logger.info(f"A processar página {page}...")
        response = requests.get(
            "https://api.github.com/users/torvalds/repos",
            params={"page": page, "per_page": 5},
            timeout=10
        )
        response.raise_for_status()
        repos = response.json()
        if not repos:
            break
        total_repos.extend(repos)
        
        # Guardar checkpoint
        context['ti'].xcom_push(key='paginas_processadas', value=page)
        logger.info(f"Checkpoint guardado: página {page}")
    
    logger.info(f"Total extraído: {len(total_repos)} repos")
    return len(total_repos)

def validar_dados(**context):
    total = context['ti'].xcom_pull(task_ids='extrair_com_checkpoint')
    if total == 0:
        raise ValueError("Nenhum dado extraído — pipeline abortado")
    logger.info(f"Validação passou: {total} registos extraídos")

default_args = {
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id='dag_failure_handling',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    default_args=default_args,
    tags=['exemplo', 'failure_handling']
) as dag:

    task_extrair = PythonOperator(
        task_id='extrair_com_checkpoint',
        python_callable=extrair_com_checkpoint
    )

    task_validar = PythonOperator(
        task_id='validar_dados',
        python_callable=validar_dados
    )

    task_extrair >> task_validar