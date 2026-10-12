from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)

def alertar_falha(context):
    """Callback que corre quando uma task falha."""
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    run_id = context['run_id']
    exception = context.get('exception')
    
    # Em produção enviarias email ou mensagem Slack aqui
    # Por agora só fazemos log
    logger.error(f"ALERTA: Task falhou!")
    logger.error(f"DAG: {dag_id}")
    logger.error(f"Task: {task_id}")
    logger.error(f"Run ID: {run_id}")
    logger.error(f"Erro: {exception}")

def alertar_sucesso(context):
    """Callback que corre quando o DAG termina com sucesso."""
    dag_id = context['dag'].dag_id
    logger.info(f"SUCESSO: DAG {dag_id} concluído com sucesso.")

def tarefa_que_pode_falhar():
    if random.random() < 0.7:
        raise Exception("Falha simulada para testar alertas!")
    logger.info("Tarefa concluída com sucesso.")

default_args = {
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
    'on_failure_callback': alertar_falha,
}

with DAG(
    dag_id='dag_com_alertas',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    default_args=default_args,
    on_success_callback=alertar_sucesso,
    tags=['exemplo', 'alertas']
) as dag:

    task_principal = PythonOperator(
        task_id='tarefa_principal',
        python_callable=tarefa_que_pode_falhar
    )