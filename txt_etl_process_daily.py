from datetime import datetime
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.branch_operator import BranchPythonOperator

# functions:
from get_data import get
from transform_data import process
from load_data import load

dag = DAG(dag_id="txt_etl_process_daily", schedule_interval="@daily", start_date=datetime.now())

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'email_on_failure': "mslusarski2@gmail.com",
    'email_on_retry': "mslusarski2@gmail.com",
}

def get_data_func():
    data = get()
    return data

def transform_data_func(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids='get_details')
    transformed_data = process(data)
    ti.xcom_push(key='transformed_data', value=transformed_data)

def load_data_func(**context):
    ti = context['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_text_task')
    loaded_data = load(transformed_data)
    return loaded_data

def send_email_func(**context):
    ti = context['ti']
    loaded_data = ti.xcom_pull(task_ids='load_text_task')
    email_body = f"The loaded data: {loaded_data}"
    
    email_notification = EmailOperator(
        task_id="email_notification",
        to="mslusarski2@gmail.com",
        subject="ETL Process Daily - Airflow DAG Execution",
        html_content=email_body,
        dag=dag,
    )
    
    email_notification.execute(context)

get_text_task = PythonOperator(
    task_id="get_details",
    python_callable=get_data_func,
    dag=dag,
)

def check_data_and_send_email(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids='get_details')
    if data is None:
        return 'send_email_notification'
    else:
        return 'transform_text_task'

check_data_task = BranchPythonOperator(
    task_id="check_data",
    python_callable=check_data_and_send_email,
    provide_context=True,
    dag=dag,
)

transform_text_task = PythonOperator(
    task_id="transform_text_task",
    python_callable=transform_data_func,
    provide_context=True,
    dag=dag
)

load_text_task = PythonOperator(
    task_id="load_text_task",
    python_callable=load_data_func,
    provide_context=True,
    dag=dag
)

send_email_notification = DummyOperator(
    task_id="send_email_notification",
    dag=dag,
)

get_text_task >> check_data_task
check_data_task >> transform_text_task
check_data_task >> send_email_notification
transform_text_task >> load_text_task
load_text_task >> send_email_notification
