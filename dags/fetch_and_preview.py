from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import pandas as pd 
from datetime import datetime, timedelta 


def get_date(**kwargs):
    url = 'https://raw.githubusercontent.com/Ayaindeed/ATP_analysis_Airbnb_price_Estimation/main/Datasets/tournaments_2020-2022.csv'
    response = requests.get(url)


    if requests.status_code == 200:
        df = pd.read_csv(url, header=None, names=['tourn_type', 'tourn_name', 'tourn_id'])

        json_data = df.to_json(orient='records')

        kwargs['ti'].xcom_push(key='tournaments_data', value=json_data)
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

def preview_data(**kwargs):
    output_data = kwargs['ti'].xcom_pull(key='tournaments_data', task_id = 'get_data')
    print(output_data)
    if output_data: 
        output_data = json.loads(output_data)
    else: 
        raise ValueError("No data found in XCom for key 'tournaments_data'")
    
    df = pd.DataFrame(output_data)
    
    print(df.head())
    



default_args = {
    'owner': 'datamasterylab.com',
    'start_date' : datetime(2026, 9, 2),
    'catchup' : 'False'
}

dag = DAG (
    'fetch_and_preview',
    default_args = default_args,
    schedule = timedelta(days = 1)
)

get_data_from_url = PythonOperator(
    task_id = 'get_data',
    python_callable = get_date,
    dag = dag
)

preview_data_from_url = PythonOperator(
    task_id = 'preview_data',
    python_callable = preview_data
    dag = dag 
)

get_data_from_url >> preview_data_from_url
