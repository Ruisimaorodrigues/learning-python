from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import csv
from pathlib import Path

logger = logging.getLogger(__name__)

def criar_csv():
    # Cria um CSV de exemplo dentro do container
    data = [
        {'id': 1, 'nome': 'Alice', 'valor': 100},
        {'id': 2, 'nome': 'Bob', 'valor': 200},
        {'id': 3, 'nome': 'Carlos', 'valor': 300},
    ]
    path = Path('/tmp/dados.csv')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nome', 'valor'])
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"CSV criado em {path} com {len(data)} linhas")
    return str(path)

def processar_csv(**context):
    path = context['ti'].xcom_pull(task_ids='criar_csv')
    total = 0
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += int(row['valor'])
    logger.info(f"Total processado: {total}")
    return total

def gerar_relatorio(**context):
    total = context['ti'].xcom_pull(task_ids='processar_csv')
    logger.info(f"Relatório: valor total = {total}")

with DAG(
    dag_id='dag_script_python',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    tags=['exemplo', 'python']
) as dag:

    task_criar = PythonOperator(
        task_id='criar_csv',
        python_callable=criar_csv
    )

    task_processar = PythonOperator(
        task_id='processar_csv',
        python_callable=processar_csv
    )

    task_relatorio = PythonOperator(
        task_id='gerar_relatorio',
        python_callable=gerar_relatorio
    )

    task_criar >> task_processar >> task_relatorio