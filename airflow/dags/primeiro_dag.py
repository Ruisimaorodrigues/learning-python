from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def extrair():
    logger.info("A extrair dados...")

def transformar():
    logger.info("A transformar dados...")

def carregar():
    logger.info("A carregar dados...")

with DAG(
    dag_id='primeiro_dag',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    tags=['exemplo']
) as dag:

    task_extrair = PythonOperator(
        task_id='extrair',
        python_callable=extrair
    )

    task_transformar = PythonOperator(
        task_id='transformar',
        python_callable=transformar
    )

    task_carregar = PythonOperator(
        task_id='carregar',
        python_callable=carregar
    )

    task_extrair >> task_transformar >> task_carregar