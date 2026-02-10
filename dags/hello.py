from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta 

default_args = {
    'owner': 'datamasterylab.com',
    'start_date' : datetime(2026, 9, 2),
    'catchup' : 'False'
}

dag = DAG (
    'hello_world',
    default_args = default_args,
    schedule = timedelta(days = 1)
)

t2 = BashOperator(
    task_id = 'print_hello',
    bash_command = 'echo "Hello World"',
    dag = dag
)

t1 = BashOperator(
    task_id = 'print_dml',
    bash_command = 'echo "Hello World"',
    dag = dag
)

t1 >> t2
