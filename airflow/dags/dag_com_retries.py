from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)

# Default args aplicam-se a todas as tasks do DAG
default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': False,
}

def tarefa_instavel():
    # Simula uma tarefa que falha aleatoriamente
    if random.random() < 0.5:
        raise Exception("Falha simulada!")
    logger.info("Tarefa concluída com sucesso.")

with DAG(
    dag_id='dag_com_retries',
    start_date=datetime(2026, 10, 1),
    schedule='@hourly',
    catchup=False,
    default_args=default_args,
    dagrun_timeout=timedelta(minutes=10),
    tags=['exemplo', 'retries']
) as dag:

    task_instavel = PythonOperator(
        task_id='tarefa_instavel',
        python_callable=tarefa_instavel
    )