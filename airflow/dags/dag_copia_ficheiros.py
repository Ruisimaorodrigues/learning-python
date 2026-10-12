from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='dag_copia_ficheiros',
    start_date=datetime(2026, 10, 1),
    schedule='@daily',
    catchup=False,
    tags=['exemplo', 'bash']
) as dag:

    criar_ficheiro = BashOperator(
        task_id='criar_ficheiro',
        bash_command='echo "dados de exemplo" > /tmp/source.txt && echo "Ficheiro criado"'
    )

    copiar_ficheiro = BashOperator(
        task_id='copiar_ficheiro',
        bash_command='cp -f /tmp/source.txt /tmp/destination.txt && echo "Ficheiro copiado"'
    )

    verificar_ficheiro = BashOperator(
        task_id='verificar_ficheiro',
        bash_command='cat /tmp/destination.txt'
    )

    criar_ficheiro >> copiar_ficheiro >> verificar_ficheiro